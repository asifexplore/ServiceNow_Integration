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
    console.log(modelOffboardBtn.dataset)
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
