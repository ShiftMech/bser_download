from flask import Flask,render_template,send_file, make_response
import pandas as pd
import requests
import os

app = Flask(__name__)

@app.route('/bser/<start>/<end>')
def bser(start,end):
    try:
        url = "http://rajresults.nic.in/resbserx19.asp"
        data = dict()
        d=  {}
        # print("1")
        for number in range(int(start),int(end)):

            payload = "roll_no="+str(number)+"&B1=Submit"
            headers = {
              'Host': 'rajresults.nic.in',
              'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Language': 'en-US,en;q=0.5',
              'Accept-Encoding': 'gzip, deflate',
              'Content-Type': 'application/x-www-form-urlencoded',
              'Content-Length': '25',
              'Origin': 'http://rajresults.nic.in',
              'Connection': 'keep-alive',
              'Referer': 'http://rajresults.nic.in/resbserx19.htm',
              'Upgrade-Insecure-Requests': '1',
              'Cache-Control': 'max-age=0'
            }

            response = requests.request("POST", url, headers=headers, data = payload)
            print(response.status_code)
            resp = pd.read_html(response.text.encode('utf8'))


            resp[2].columns=resp[2].iloc[0,:].tolist()
            resp[2] = resp[2][1:]
            resp[2].set_index('Name',inplace=True)

            for ind in resp[2].index:
                if ind.startswith(('Total','Percentage','Result')):
                    resp[2] = resp[2].drop(ind)
            marks = resp[2].stack().to_frame().T


            resp[1].set_index(0,inplace=True)

            info = resp[1].stack().to_frame().T
            info.reset_index(inplace=True)

            final = info.merge(marks,how='outer',right_index=True,left_index=True)
            d[number] = final
        output = pd.concat(d, axis=0)
        output.drop(columns=['index'],inplace=True)
        output.to_excel(os.path.join(os.getcwd(),'result.xlsx'))
        #return send_file(os.path.join(os.getcwd(),'result.xlsx'),as_attachment=True)

	response = make_response(send_file(os.path.join(os.getcwd(),'result.xlsx'),as_attachment=True))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response
        # return output
    except Exception as e:
        print(e.args[0])
        return None

if __name__ == '__main__':
	app.run()
