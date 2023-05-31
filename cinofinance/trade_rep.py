import pytr
import os

os.system("pytr login")




# Use "pytr command_name --help" to get detailed help to a specific command

# Commands:
#   {help,login,dl_docs,portfolio,details,get_price_alarms,set_price_alarms,export_transactions,completion}
#                          Desired action to perform
#     help                 Print this help message
#     login                Check if credentials file exists. If not create it and ask for input. Try to login. Ask for device reset if needed
#     dl_docs              Download all pdf documents from the timeline and sort them into folders. Also export account transactions (account_transactions.csv) and JSON files with all events (events_with_documents.json and
#                          other_events.json
#     portfolio            Show current portfolio
#     details              Get details for an ISIN
#     get_price_alarms     Get overview of current price alarms
#     set_price_alarms     Set price alarms based on diff from current price
#     export_transactions  Create a CSV with the deposits and removals ready for importing into Portfolio Performance
#     completion           Print shell tab completion

# optional arguments:
#   -h, --help             show this help message and exit
#   -v {warning,info,debug}, --verbosity {warning,info,debug}
#                          Set verbosity level (default: info)
#   -V, --version          Print version information and quit
