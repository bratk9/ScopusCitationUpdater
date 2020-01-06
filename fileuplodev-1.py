from flask import Flask, render_template, request, make_response
import csv
import os
import weasyprint

app = Flask(__name__)

@app.route('/')
def uploadfile():
   return render_template('upload.html')
	
@app.route('/uploader',methods=['GET','POST'])
def getpostmet():
    if request.method=='GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        file = request.files['file']
        file.stream.seek(0)
        myfile=file.read().decode("utf-8")
        data=csv.reader(myfile.split('\n'),delimiter=',')
        generated=[]
        for info in data:
            #code for getting citation  :  todo
            generated.append(info)
            #append profassor info and citation to info
        pdf_outline=render_template('pdf_template.html',result=generated)
        # pdf=pdfkit.from_string(pdf_outline,False)

        pdf=weasyprint.HTML(string=pdf_outline).write_pdf()

        resp=make_response(pdf)
        resp.headers['Content-Type']="application/pdf"
        resp.headers['Content-Disposition']="inline;filename=Citations.pdf"

        return resp
        
if __name__ == '__main__':
   app.run(debug = True)