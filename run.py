from booking.booking import Booking
import time

try:
    with Booking() as bot:
        bot.land_first_page()
        #bot.change_currency(currency='SGD')
        bot.select_place_to_go(input("Where do you want to go?"))
        bot.select_dates(check_in_date=input("When do you want to check in?"), check_out_date=input("When do you want to check out?"))
        bot.select_adults(int(input('How many adults?')))
        bot.click_search()
        bot.apply_filtrations()
        #time.sleep(5)
        bot.refresh()
        bot.report_results()

except Exception as e:
    if 'in PATH' in str(e):
        print('You are trying to run the bot from CML.\n'
        'Please add to PATH your Selenium Drivers \n'
        'Windows: \n'
        '    set PATH=%PATH%;C:path-to-your-folder \n \n'
        'Linux: \n'
        '     PATH=$PATH:/path/toyour/folder/ \n')
    else:
        raise
