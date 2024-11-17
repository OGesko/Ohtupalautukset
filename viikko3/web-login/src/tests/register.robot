*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Input Username  validuser
    Input Password  validpsw123
    Input Password Confirmation  validpsw123
    Submit Registration
    Register Should Be Successful

Register With Too Short Username And Valid Password
    Input Username  ab
    Input Password  validpsw123
    Input Password Confirmation  validpsw123
    Submit Registration
    Page Should contain  username too short!

Register With Valid Username And Too Short Password
    Input Username  validuser2
    Input Password  abcd567
    Input Password Confirmation  abcd567
    Submit Registration
    Page Should contain  password too short!

Register With Valid Username And Invalid Password
    Input Username  validuser3
    Input Password  nonumbers
    Input Password Confirmation  nonumbers
    Submit Registration
    Page Should contain  invalid password!

Register With Nonmatching Password And Password Confirmation
    Input Username  validuser4
    Input Password  validpsw999
    Input Password Confirmation  diffbutvalid999
    Submit Registration
    Page Should contain  password confirmation failed!

Register With Username That Is Already In Use
    Input Username  samename
    Input Password  validpsw345
    Input Password Confirmation  validpsw345
    Submit Registration
    Go To Register Page
    Input Username  samename
    Input Password  validpsw567
    Input Password Confirmation  validpsw567
    Submit Registration
    Page Should contain  User with username samename already exists

*** Keywords ***
Input Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Input Password
    [Arguments]  ${password}
    Input Text  password  ${password}

Input Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Text  password_confirmation  ${password_confirmation}

Submit Registration
    Click Button  Register

Register Should Be Successful
    Welcome Page Should Be Open

Reset Application And Go To Register Page
    Reset Application
    Go To Register Page