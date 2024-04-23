from flask import Flask, render_template, request

app = Flask(__name__)

# Mock list of services
services = ['Service 1', 'Service 2', 'Service 3']

relationships = {}

@app.route('/relations')
def home():
    return render_template('webview.html', services=services, relationships=relationships)

@app.route('/define_relationship', methods=['POST'])
def define_relationship():
    service1 = request.form.get('service1')
    service2 = request.form.get('service2')
    relationship = request.form.get('relationship')
    condition_type = request.form.get('condition_type')

    # Here you can handle the relationship between the services
    # For example, save it to a database

    if condition_type == 'order_based':
        # Add service2 directly under service1
        relationships[service1] = service2
    elif condition_type == 'condition_based':
        # Check if service1 already has a condition-based relationship
        if service1 in relationships and isinstance(relationships[service1], dict):
            # Add service2 under service1 with the condition as the key
            relationships[service1][relationship] = service2
        else:
            # Add service2 under service1 with the condition as the key
            relationships[service1] = {relationship: service2}

    return  render_template('webview.html', services=services, relationships=relationships)

if __name__ == '__main__':
    app.run(debug=True)