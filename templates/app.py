from flask import Flask, render_template, request, flash
import messagebird
import random

#Configure the app as follows.
app = Flask(__name__)
app.config.from_pyfile('config_file.cfg')

#create instance of messagebird.Client using API key
client = messagebird.Client(app.config['SECRET_KEY'])

#Route for the appointment form. Determines what happens when form is submitted.
@app.route('/', methods=['GET', 'POST'])
def callMe():
    
    #when form is submitted
    if request.method=="POST":

        #make array of sales agent numbers. We'll send the SMS to a random choice from this array.
        numbers = app.config['SALES_AGENT_NUMBERS'].split(",")

        #try submitting to MessageBird client
        try:
            verify = client.message_create('M. B. Cars', random.choice(numbers),                             "You have a new lead: " + request.form['customer_name'] + ". Call them at " + request.form['phone'])

            #on succcess, redirect the user to the confirmation page 
            return render_template('success.html', name=request.form['customer_name'], phone=request.form['phone']) 
       
        #on failure, flash error on webpage.
        except messagebird.client.ErrorException as e:
            for error in e.errors:
                print (error)
                flash('  description : %s\n' % error.description)
            return render_template('index.html')            

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
