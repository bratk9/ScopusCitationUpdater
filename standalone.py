from flask import Flask, render_template, request, make_response
import requests
import csv
import io
import json
from reportlab.platypus import Table
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import TableStyle
from reportlab.lib import colors

ts=TableStyle([
    ('BACKGROUND',(0,0),(-1,0),colors.blue),
    ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
    ('GRID',(0,0),(-1,-1),1,colors.black)
])

app = Flask(__name__)

@app.route('/')
def uploadfile():
   return render_template('upload.html')
	
@app.route('/uploader',methods=['GET','POST'])
def getpostmet():
    if request.method=='GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        buf=io.BytesIO()
        file = request.files['file']
        if file:
            file.stream.seek(0)
            myfile=file.read().decode("utf-8")
            data=csv.reader(myfile.split('\n'),delimiter=',')
            generated=[["Name","ORCID","Citation"]]
            for info in data:

                if(info and len(info)!=0 and info[1] and len(info[1])!=0 and info[0] and len(info[0])!=0):
                    res=requests.get("http://api.elsevier.com/content/author",
                                        params={"orcid":info[1]},
                                        headers={'Accept':'application/json',
                                        'X-ELS-APIKey': '24783270e58eb56ff94c059e8c7eb44c'})
                    respdat=dict(res.json())
                    if list(respdat)[0]=="service-error":
                        print(info[0],"error")
                    else:
                        print(info[0],respdat['author-retrieval-response'][0]['coredata']['citation-count'])
                        generated.append([info[0],info[1],respdat['author-retrieval-response'][0]['coredata']['citation-count']])
            table=Table(generated)
            table.setStyle(ts)
            pdfcreator=SimpleDocTemplate(buf)
            pdfcreator.build([table])
            pdf=buf.getvalue()
            buf.close()
            resp=make_response(pdf)
            resp.headers['Content-Type']="application/pdf"
            resp.headers['Content-Disposition']="inline;filename=Citations.pdf"
            print("sent")
            return resp
        else:
            return render_template('upload.html')
        
if __name__ == '__main__':
   app.run(debug = True)