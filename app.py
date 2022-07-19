import json
from locale import currency
from flask import Flask, request
import requests


app = Flask(__name__)




# second endpoint
@app.route('/bankwebhook', methods=['GET', 'POST'])     # get the data i.e amount returned by the bank
def bank_webhook(): 
    
        
    # handle the POST request
    # for testing
    if request.method == 'POST':           
        amount=request.form.get('amount')
        currency=request.form.get('currency')        

        return '''  <h1> The amount is {}</h1>
                    <h1> The currency is {}</h1> '''.format(amount,currency )

    return '''
           <form method="POST">
               <div>amount: <input type="text" name="language"></div>
               <div>currency: <input type="text" name="framework"></div>
               <input type="submit" value="Submit">
           </form>'''

    pass 

    
# send the details to erply
# @app.route('/')
def savePay(): # after paying

    url = "https://516378.erply.com/api?"

    payload = {
            
               'bankSum': '25.00',
               'date': '2022-07-15 08:10:19',
               'bankReferenceNumber': '091520151759',
               'bankCurrency': 'ZAR',
               'statusCode':'complete',
               }
    
    
    
   # params = {'sessionKey': '8beefa9dd05141c320ec2a3a6ab50d57f2f47d84b8f9', }

  
    headers = {
        'Cookie': 'PHPSESSID-516378=b8da5d4c8cedea244f0080d1190bc54c',        
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8',  
        'clientCode': '516378',
           

    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    print(response.text)

    
    

# send https://learn-api.erply.com/requests/savepayment



 # first endpoint
@app.route('/pay/<reference>')
def pay(reference):
    invoiceData = getInvoiceData(reference)
    #print(invoiceData)
    

    linkData= getpaymentLink(invoiceData)
   # trim null from linkData
  
   
    data=json.loads(linkData)
    # redirect to the link item in that data
    print(data)
    return reference
    pass


     # get invoice data from erply
    # return invoice data
def getpaymentLink(invoiceData):

    url = "https://gateway.bms.co.za/api/v1/express/get-link"

    payload = {'amount': '1',
               'reference': '2'}

    headers = {
        'Authorization': 'Basic Y2FwZXdhdGNodHNvZ2E6V283WW9sOGhSOUt1',
        'Cookie': 'PHPSESSID=3iruhe8pmupgr4p169vrp4vsaq; _csrf=deb196623918cedadbf6e3f4aeb443eb1861ea5fe69a610749cebb3943abcb2fa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22G3fYmgd6oMTvcpny09d6Fgo4wkdPG4GL%22%3B%7D'
    }

    response = requests.request("POST", url, headers=headers, data=payload,)

    print(response.text)


 # call bank api ang generate payment link
  # parse linkdata get payment link and redirect
def getInvoiceData(reference):
    sessionkey= getsession()
    url = "https://516378.erply.com/api?request=getSalesDocuments&id="+reference+"&sessionKey="+sessionkey+"&clientCode=516378"


    headers = {
        'clientCode': '516378',
        'sessionKey': '8beefa9dd05141c320ec2a3a6ab50d57f2f47d84b8f9',
        'Content-Type': 'text/plain',
        'Cookie': 'PHPSESSID-516378=b8da5d4c8cedea244f0080d1190bc54c'
    }

    response = requests.request("POST", url, headers=headers)    

    print(response.text)
    pass



def getsession(): # after paying


    url = "https://516378.erply.com/api?request=verifyUser&password=2rBk907sanXv&username=johnmuchemi@tsogatec.co.za&clientCode=516378"

    payload = {'request': 'verifyUser',
               'password': '2rBk907sanXv',
               'username': 'johnmuchemi@tsogatec.co.za',
               'clientCode': '516378'}
    files = [

    ]
    headers = {
        'Cookie': 'PHPSESSID-516378=b8da5d4c8cedea244f0080d1190bc54c'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(response.text)
    userdata = json.loads(response.text)
    sessionKey=userdata['records'][0]['sessionKey']
    return sessionKey


    pass

    # put application's code here
# pick ref no and call api to get the amount to be paid '
# call the bank api to get a payment link
# redirect to payment link


if __name__ == '__main__':
    app.run()
