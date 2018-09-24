# Instant Lead Alerts
### ⏱ 15 min build time

## Why build instant lead alerts for Sales? 

Even though a lot of business transactions happen on the web, talking on the phone can be more effective from the business' and user's perspectives. Personal contact is often essential for high-value transactions in industries such as real estate and the mobility industry.

One way to streamline this workflow is by building callback forms on your website. Through these forms, customers can enter their contact details and receive a phone call, thus skipping queues where they need to stay on hold. 

Callback requests reflect a high level of purchase intent and should be dealt with as soon as possible to increase the chance of converting a lead. Therefore it's paramount to get them pushed to a sales agent as quickly as possible. SMS messaging has proven to be one of the most instant and effective channels for this use case.

In this MessageBird Developer Guide, we'll show you how to implement a callback form on a Python-based website with SMS integration. The form will collect leads for our fictitious car dealership, M.B. Cars.

## Getting Started

You need to have Python and the [Flask](http://flask.pocoo.org/docs/0.12/) framework installed on your machine to run the sample application. You can use the Python package manager [pip](https://pip.pypa.io/en/stable/) to install Flask as follows:

````bash
pip install Flask
```` 

The source code is available in the [MessageBird Developer Guides GitHub repository](https://github.com/messagebirdguides/lead-alerts-guide-python) from which it can be cloned or downloaded into your development environment.

After saving the code, open a console for the download directory and run the following command, which installs the MessageBird Python client:

````bash
pip install messagebird
````

## Configuring the MessageBird Client

The MessageBird Python client is used to send messages. It's added as a dependency and loaded with the following lines in `app.py`:

````python
#create instance of messagebird.Client using API key
client = messagebird.Client(app.config['SECRET_KEY'])
````

You need an API key, which you can retrieve from [the MessageBird dashboard](https://dashboard.messagebird.com/en/developers/access). As you can see in the code example above, the key is set as a parameter when instantiating the MessageBird Python client, and it's loaded from an environment variable called SECRET_KEY. We define configuration variables in the file `config_file.cfg`. Edit this file to use your own API key.

In the same file, we specify the sales agents' telephone numbers. These are the recipients that will receive the SMS alerts when a potential customer submits the callback form. You can separate multiple numbers with commas. In our application, you'll have to include the country code with the numbers.

You can also specify additional Flask configuration variables. When testing your application, it's often useful to set the variable `DEBUG` to `True`.

Here's an example of a valid configuration file for our sample application:

````env
SECRET_KEY='YOUR_API_KEY'
DEBUG=True
SALES_AGENT_NUMBERS = '+1312XXXXXXX, +1412XXXXXXX'
````

## Showing a Landing Page

The landing page is a simple HTML page with information about our company, a call to action and a form with two input fields, name and number, and a submit button. We use Jinja templates for our HTML pages. You can see the landing page in the file `templates/index.html`. The `@app.route('/', methods=['GET', 'POST'])` route in `app.py` is responsible for rendering it.

## Handling Callback Requests

When the user submits the form, the `app.post('/callMe')` route receives their name and number from the HTML form. These fields are marked as "required" in our `index.html` template.

First, we define where to send the message. As you've seen above, we specified multiple recipient numbers in the `SALES_AGENT_NUMBERS` configuration variable. M.B. Cars has decided to randomly distribute incoming calls to their staff so that every salesperson receives roughly the same number of leads. We do this by constructing a list from the comma-separated value of `SALES_AGENT_NUMBERS`. Later, when creating the message, we use a random number from the list by using `random.choice(numbers)` as the recipient's number.

````python
#when form is submitted
if request.method=="POST":
    #make array of sales agent numbers. We'll send the SMS to a random choice from this array.
    numbers = app.config['SALES_AGENT_NUMBERS'].split(",")
````

Now we can formulate a message for the agent and send it through the MessageBird client using the `message_create()` method:

````python
#try submitting to MessageBird client
try:
    verify = client.message_create('M. B. Cars', 
    		 random.choice(numbers),                         
    		 "You have a new lead: " + request.form['customer_name'] + ". Call them at " + request.form['phone'])
````

There are three parameters:

- "M. B. Cars": This is the sender ID---the message will appear to come from a source with this name.
- `random.choice(numbers)`: A random element from the `numbers` list defined earlier. The API supports an array of recipients; in this case we're sending the message to only one number, so we don't use an array.
- The text of the message, including variables from the form inputs.

If the message is successfully created, we display a success page confirming the prospective customer's information:

````python
#on succcess, redirect the user to the confirmation page 
return render_template('success.html', 	
						name=request.form['customer_name'], 
						phone=request.form['phone']) 
````

The success page follows the template stored at `templates/success.html`.

If there's an error while creating the message, we print the error to the console and flash its description above the form:

````python
#on failure, flash error on webpage.
except messagebird.client.ErrorException as e:
    for error in e.errors:
        print (error)
        flash('  description : %s\n' % error.description)
    return render_template('index.html')  
````

## Testing the Application

Have you edited your `config_file.cfg` file to contain a working key and added your phone number to the existing phone numbers, as explained above in _Configuring the MessageBird Client_, to receive the lead alert? Awesome!

Now run the following command from your console:

````bash
python app.py
````

Go to http://localhost:5000/ to see the form and request a lead!

## Nice work!

You've just built your own instant lead alerts application with MessageBird! 

You can now use the flow, code snippets and UI examples from this tutorial as an inspiration to build your own SMS-based lead alerts application. Don't forget to download the code from the [MessageBird Developer Guides GitHub repository](https://github.com/messagebirdguides/lead-alerts-guide-python).

## Next steps

Want to build something similar but not quite sure how to get started? Please feel free to let us know at support@messagebird.com, we'd love to help!