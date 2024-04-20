
// Simulated data for things
var thingsData = [
    { id: 1, name: "Thing 1", description: "Description for Thing 1", services: ["Service A", "Service B", "Service C"] },
    { id: 2, name: "Thing 2", description: "Description for Thing 2", services: ["Service X", "Service Y", "Service Z"] },
    { id: 3, name: "Thing 3", description: "Description for Thing 3", services: ["Service M", "Service N", "Service O"] }
];

// Simulated data for relationships
var relationshipsData = [
    { serviceA: "Service A", serviceB: "Service B", type: "Order-based" },
    { serviceA: "Service C", serviceB: "Service Z", type: "Condition-based" },
    // Add more relationships as needed
];

// Function to populate Things tab with data
function populateThingsTab() {
    var thingsList = document.getElementById("thingsList");
    thingsList.innerHTML = ""; // Clear previous content

    // Loop through things data and create HTML elements
    for (var i = 0; i < thingsData.length; i++) {
        var thing = thingsData[i];
        var thingDiv = document.createElement("div");
        thingDiv.classList.add("thing");
        thingDiv.innerHTML = "<strong>Name:</strong> " + thing.name + "<br><strong>Description:</strong> " + thing.description;
        thingsList.appendChild(thingDiv);
    }
}

// Function to populate Services tab with data
function populateServicesTab() {
    var servicesList = document.getElementById("servicesList");
    servicesList.innerHTML = ""; // Clear previous content

    // Loop through things data
    for (var i = 0; i < thingsData.length; i++) {
        var thing = thingsData[i];
        var thingDiv = document.createElement("div");
        thingDiv.innerHTML = "<h4>" + thing.name + "</h4>";

        // Sort services alphabetically
        thing.services.sort();

        // Create list of services for each thing
        var servicesListForThing = document.createElement("ul");
        for (var j = 0; j < thing.services.length; j++) {
            var service = thing.services[j];
            var serviceItem = document.createElement("li");
            serviceItem.textContent = service;
            servicesListForThing.appendChild(serviceItem);
        }
        thingDiv.appendChild(servicesListForThing);
        servicesList.appendChild(thingDiv);
    }
}

// Function to populate Relationships tab with data
function populateRelationshipsTab() {
    var relationshipsList = document.getElementById("relationshipsList");
    relationshipsList.innerHTML = ""; // Clear previous content

    // Loop through relationships data and create table rows
    for (var i = 0; i < relationshipsData.length; i++) {
        var relationship = relationshipsData[i];
        var row = document.createElement("tr");
        row.innerHTML = "<td>" + relationship.serviceA + "</td>" +
                        "<td>" + relationship.serviceB + "</td>" +
                        "<td>" + relationship.type + "</td>";
        relationshipsList.appendChild(row);
    }
}

// Function to switch to the Apps tab and clear the editor
function startNewApp() {
    openTab(event, 'apps');
    clearEditor();
}

// Function to switch to the Apps tab and prompt for uploading existing app
function uploadExistingApp() {
    openTab(event, 'apps');
    var existingApp = prompt("Please paste your existing app code here:");
    if (existingApp != null) {
        document.getElementById("appEditor").value = existingApp;
    }
}

// Function to save the app locally
function saveApp() {
    // You can implement saving functionality here
    alert("App saved successfully!");
}

// Function to clear the editor
function clearEditor() {
    document.getElementById("appEditor").value = "";
}

// Function to finalize the app
function finalizeApp() {
    var appName = prompt("Please enter a name for your app:");
    if (appName != null && appName.trim() !== "") {
        // You can implement finalizing functionality here
        alert("App finalized successfully with name: " + appName);
    } else {
        alert("Please enter a valid name for your app.");
    }
}

// Function to activate the app
function activateApp() {
    // You can implement activation functionality here
    alert("App activated successfully!");
}

// Function to stop the app
function stopApp() {
    // You can implement stopping functionality here
    alert("App stopped successfully!");
}

// Function to delete the app
function deleteApp() {
    // You can implement deletion functionality here
    alert("App deleted successfully!");
}

// JavaScript function to switch between tabs
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    // If the Things tab is clicked, populate it with data
    if (tabName === "things") {
        populateThingsTab();
    } else if (tabName === "services") {
        populateServicesTab();
    } else if (tabName === "relationships") {
        populateRelationshipsTab();
    }
}

// Initially populate the Things tab with data
populateThingsTab();