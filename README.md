# liveupstoxoc
## Fetch live OptionsChain from Upstox for free

Pypi : https://pypi.org/project/liveupstoxoc/

## Installation

Make sure you've installed chromedriver as per your systen. 
If not use download chromedrivers from https://chromedriver.storage.googleapis.com/index.html?path=95.0.4638.17/


```sh
pip install liveupstoxoc
```


## How to use the library

```sh
n = live_upstox_oc.upstox_oc(path to chromedriver)
#Now enter login details of your upstox account
n.login(username, password, 2fa)
#Now you're ready for fetch live options chain. 
#For fetching optionschain of NIFTY and BANKNIFTY
oc = n.get_oc("NIFTY") # or "BANKNIFTY"
#For fetching optionschain of Stocks
oc = n.get_oc("3426") #For fetching option chain of TataPower. Similarly enter Token of the stocks you want to Fetch options chain for. 
#To close the chromedriver
n.close()
```
