function checkPass()
{
    //Store the password field objects into variables ...
    var password = document.getElementById('pass');
    var confirm  = document.getElementById('re_pass');
    //Set the colors we will be using ...
    var good_color = "#66cc66";
    var bad_color  = "#ff6666";
    //Compare the values in the password field
    //and the confirmation field
    if(password.value == confirm.value){
        //The passwords match.
        //Set the color to the good color and inform
        //the user that they have entered the correct password
        confirm.style.backgroundColor = good_color;
        message.style.color           = good_color;
    }else{
        //The passwords do not match.
        //Set the color to the bad color and
        //notify the user.
        confirm.style.backgroundColor = bad_color;
        message.style.color           = bad_color;
    }
}