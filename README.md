from Travian import Travian

url_main = 'https://ts1.balkans.travian.com/'
username = 'email'
password = 'password'

T = Travian(username, password, url_main)
T.login()
