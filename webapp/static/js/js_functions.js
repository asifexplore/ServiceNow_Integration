console.log("Running")
var onboardBtnModalz = document.getElementById('onBoardBtnJs')

onboardBtnModalz.addEventListener('click', function(){
    console.log("Success Button clicked")
    // Append information to the fields
    var btnData = onboardBtnModalz.dataset.product
    btnData = btnData.replaceAll(`'`, `"`)
    var obj = JSON.parse(btnData);
    var platformAndSafes =  document.getElementById('platformAndSafes').value
    platformAndSafes = platformAndSafes.replaceAll(`'`, `"`)
    platformAndSafes = JSON.parse(platformAndSafes);
    // console.log(platformAndSafes)
    // console.log(typeof(platformAndSafes))
    platformSelect = document.getElementById('platformDropdown');
    safeSelect = document.getElementById('safeDropdown');

    platformArray = Object.keys(platformAndSafes)
    // console.log(platformArray)

    for (let i = 0; i < platformArray.length; i++){
        platformSelect.options.add( new Option(platformArray[i],platformArray[i]) )
    }

    // Getting value of first option
    var safeValue = platformAndSafes[platformArray[0]]
    // console.log(safeValue)

    if(typeof safeValue === 'string'){
        safeSelect.options.add( new Option(safeValue,safeValue))
    }else{
        for (let i = 0; i < safeValue.length; i++){
            safeSelect.options.add( new Option(safeValue,safeValue))
        }
    }

    document.getElementById('accountName').value = obj['name']
    document.getElementById('address').value = obj['address']
    document.getElementById('FQDN').value = obj['fqdn']
    document.getElementById('OS').value = obj['type']


});

// Submit / Onboard Button on Modal 
var modalSubmit = document.getElementById('modalSubmit')
modalSubmit.addEventListener('click', function(){
    // Get All Information 
    var accountName = document.getElementById('accountName').value
    var address = document.getElementById('address').value 
    var fqdn = document.getElementById('FQDN').value 
    var os = document.getElementById('OS').value 
    var username = document.getElementById('username').value 
    var password = document.getElementById('password').value 

    var platformChosen = document.querySelector('#platformDropdown').value;
    var safeChosen = document.querySelector('#safeDropdown').value;

    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value

    console.log(accountName)
    console.log(address)
    console.log(fqdn)
    console.log(os)
    console.log(username)
    console.log(password)
    console.log(platformChosen)
    console.log(safeChosen)

    var url ='onboard/'
    // Ajax to Upload 
    fetch(url,
        {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrfToken,  
        }, 
        mode:'same-origin',
        body:JSON.stringify({'accountName':accountName,'address':address,'fqdn':fqdn,'os':os,'username':username,'password':password,'platformChosen':platformChosen,'safeChosen':safeChosen})
        })
        .then((respose) => {
            return respose.json();
        })
        .then((data) => {
            console.log("Inside Then")
            console.log(data)
            if (data == "Success")
            {
                location.reload()
            }

        });
});

// Offboarding JS 
// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var modelOffboardBtn = document.getElementById('offBoardingButton')
modelOffboardBtn.addEventListener('click', function(){
    console.log("Submit clicked")

    var btnData = modelOffboardBtn.dataset.product
    console.log(btnData)
    document.getElementById('deleteAccInfo').value = btnData
    
});

var modelOffSubmitBtn = document.getElementById('offboardingDeletebtn')
modelOffSubmitBtn.addEventListener('click', function(){
    console.log("Delete Confirm Button Pressed")

    var delData = document.getElementById('deleteAccInfo').value
    console.log(delData)

    delData = delData.replaceAll(`'`, `"`)
    var obj = JSON.parse(delData);
    console.log(obj)
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value

    var url ='offboard/'
    // Ajax to Upload 
    fetch(url,
        {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrfToken,  
        }, 
        mode:'same-origin',
        body:JSON.stringify({'address':address,'objData':obj})
        })
        .then((respose) => {
            return respose.json();
        })
        .then((data) => {
            console.log("Inside Then")
            console.log(data)
            if (data == "Success")
            {
                location.reload()
            }

        });
});
