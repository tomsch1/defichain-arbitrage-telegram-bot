import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import alarms
import crypto_comparison
import cexdatacollect
import dfi_dex_prices
import dfi_oracle_prices
import stock_token_comparison
import symbols
from alarms import StockAlarmConfig
import configparser

with open("application.properties", 'r') as f:
    config_string = '[default]\n' + f.read()
    f.close()
config_parser = configparser.ConfigParser()
config_parser.read_string(config_string)

def get_config(config_key):
    return config_parser.get('default', config_key)

tg_token = get_config('telegram_token')



token = tg_token


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

dex_data = dfi_dex_prices.DfiDexPrices()
cex_data = cexdatacollect.CexPriceFetch()
oracle_data = dfi_oracle_prices.DfiOraclePrices()
crypto_comparison = crypto_comparison.CryptoComparison(dex_data, cex_data)
stock_token_comparison = stock_token_comparison.StockComparison(dex_data, oracle_data)

#alarmConfig
stock_alarm_config = StockAlarmConfig(stock_token_comparison, './stock_alarms.json')
crypto_alarm_config = alarms.CryptoAlarmConfig(crypto_comparison, './crypto_alarms.json')


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.
# This being an example and not having context present confusing beginners,
# we decided to have it present as context.
def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text("""/compare_crypto to compare DFI DEX and KuCoin prices.
    /compare_stocks to compare dex d_token prices with oracle prices
    /add_stock_token_alarm [token symbol] [threshold percentage] to subscribe for an alarm on the definied thershold
    /add_crypto_token_alarm [token symbol] [threshold percentage] to subscribe for an alarm on the definied thershold
    If there is a intermittent conversion needed, only the one with maximum difference between DEX and CEX will be shown.
    Transaction and trading fees are not yet included.
    Use /compare_stocks to compare DEX stock token prices with oracle stock prices""")


def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Beep!')


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, context=chat_id, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def add_stock_token_alarm(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if context.args[0] not in symbols.StockTokenSymbols.name_list():
        print(symbols.StockTokenSymbols.list())
        update.message.reply_text(f'Symbol {context.args[0]} not found')
        return
    if not 0  < float(context.args[1]) < 1:
        update.message.reply_text(f'Threshold must be a number between 0 and 1')
        return
    #try:
    #args[0] should contain the symbol
    alarm_symbol = symbols.StockTokenSymbols.from_string(context.args[0]).name
    #args[1] should contain the threshold
    alarm_threshold = float(context.args[1])
    alarm = alarms.Alarm(alarm_symbol, alarm_threshold, str(chat_id))
    stock_alarm_config.alarmsConfig.add_alarm(alarm)
    update.message.reply_text(f'Token {alarm_symbol} added successfully with alarm threshold {alarm_threshold*100}%')
    #except BaseException as e:
        #update.message.reply_text(f'Failed to add alarm: {e}')

def add_crypto_token_alarm(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if context.args[0] not in symbols.CryptoExchangeSymbols.name_list():
        print(symbols.CryptoExchangeSymbols.list())
        update.message.reply_text(f'Symbol {context.args[0]} not found')
        return
    if not 0  < float(context.args[1]) < 1:
        update.message.reply_text(f'Threshold must be a number between 0 and 1')
        return
    #try:
    #args[0] should contain the symbol
    alarm_symbol = symbols.CryptoExchangeSymbols.from_string(context.args[0]).name
    #args[1] should contain the threshold
    alarm_threshold = float(context.args[1])
    alarm = alarms.Alarm(alarm_symbol, alarm_threshold, str(chat_id))
    crypto_alarm_config.alarmsConfig.add_alarm(alarm)
    update.message.reply_text(f'Token {alarm_symbol} added successfully with alarm threshold {alarm_threshold*100}%')
    #except BaseException as e:
        #update.message.reply_text(f'Failed to add alarm: {e}')


def evaluate_stock_alarms(context: CallbackContext) -> None:
    stock_token_comparison.update_data()
    alarms = stock_alarm_config.evaluate_list_alarms()
    for alarm in alarms:
        chat_id = list(alarm.keys())[0]
        alarm = list(alarm.values())[0]
        message = f"{alarm.symbol.name}\nOracle price: {round(alarm.oracle_price, 2)} $\nDex price: {round(alarm.dex_price, 2)} DUSD\n{round(alarm.percentage*100, 2)} %"
        context.bot.send_message(chat_id, message)

def evaluate_crypto_alarms(context: CallbackContext) -> None:
    """Send the alarm message."""
    crypto_comparison.update_pairs()
    alarms = crypto_alarm_config.evaluate_list_alarms()
    for alarm in alarms:
        chat_id = list(alarm.keys())[0]
        alarm = list(alarm.values())[0]
        print(alarm.__dict__)
        pair = alarm
        if pair.intermediate_pair is None:
            text = f"""
            DFI -> {pair.dex_dfi_pair.symbol.split('/')[1]}:
            DEX:\t{round(pair.dex_dfi_pair.price, 3)} DFI
            {pair.ex_name}:\t{round(pair.cex_dfi_pair.price, 3)} DFI
            \t{round(pair.percentage * 100, 2)} %
            """
        else:
            text = f"""
            DFI -> {pair.dex_dfi_pair.symbol.split('/')[1]}:
            DEX:\t{round(pair.dex_dfi_pair.price, 3)} DFI
            {pair.ex_name} via {pair.intermediate_pair.symbol.split('/')[1]}:\t{round(pair.cex_dfi_pair.price / pair.intermediate_pair.price, 3)} DFI
            \t{round(pair.percentage * 100, 2)} %
            """
        context.bot.send_message(chat_id, text)


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def compare_crypto(update: Update, context: CallbackContext) -> None:
    logging.info(f"Request from {update.message.chat_id}")
    text = crypto_comparison.get_overview()
    update.message.reply_text(text)

def compare_stocks(update: Update, context: CallbackContext) -> None:
    logging.info(f"Request from {update.message.chat_id}")
    text = stock_token_comparison.get_overview()
    update.message.reply_text(text)


def update_cex_data(context: CallbackContext) -> None:
    cex_data.update_all_tickers()

def update_dex_data(context: CallbackContext) -> None:
    dex_data.update_dex_crypto_tickers()
    dex_data.update_dex_stock_tickers()
    oracle_data.update_dfi_oracle_stock_tickers()


def run_bot() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    #dispatcher.add_handler(CommandHandler("help", start))
    #dispatcher.add_handler(CommandHandler("set", set_timer))
    #dispatcher.add_handler(CommandHandler("unset", unset))
    dispatcher.add_handler(CommandHandler("compare_crypto", compare_crypto))
    dispatcher.add_handler(CommandHandler("compare_stocks", compare_stocks))
    dispatcher.add_handler(CommandHandler("add_stock_token_alarm", add_stock_token_alarm))
    dispatcher.add_handler(CommandHandler("add_crypto_token_alarm", add_crypto_token_alarm))

    #start fetching data
    updater.job_queue.run_repeating(callback=update_cex_data, interval=10.0)
    updater.job_queue.run_repeating(callback=update_dex_data, interval=10.0)
    updater.job_queue.run_repeating(callback=evaluate_stock_alarms, interval=20.0)
    updater.job_queue.run_repeating(callback=evaluate_crypto_alarms, interval=20.0)



    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    run_bot()
