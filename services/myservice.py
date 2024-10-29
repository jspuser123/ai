from kivy.network.urlrequest import UrlRequest
import plyer
import time
from jnius import autoclass


PythonService=autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)
req=None
def req_fun(req,*args):
    try:
        req = UrlRequest('http://192.168.43.73/api',on_error=error_fun(),on_failure=fail_fun(),on_success=scuess_full())
        req.wait()
    except:
        plyer.notification.notify(title='RequestService', message="error expect")
def scuess_full(req,*args):
    d=req.result
    a=d['data']
    plyer.notification.notify(title='notification', message=a)
def error_fun(*args):
    plyer.notification.notify(title='RequestService', message="error reponse")
def fail_fun(*args):
    plyer.notification.notify(title='RequestService', message="fail reponse")

def test_fun(*args):
    plyer.notification.notify(title='RequestService', message="back ground funtion")
def time_fun():
    time.sleep(5)
    test_fun()
    time.sleep(5)
    test_fun()
    time.sleep(5)
    test_fun()
    time.sleep(5)
    req_fun()
    time.sleep(5)
    plyer.notification.notify(title='RequestService', message="back ground funtion_TIME")
if __name__ == "__main__":
    time_fun()