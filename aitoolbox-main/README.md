# aitoolbox
ai tool based on image processing

Installation procedure :
First inatall all the files and arrange it in the order shown in the folders
then install caffine model from the google drive link given in caffine model readme .

open project folder
left clixk on it and open terminal 
write python aitoolbox2_0.py
the flask will start hosting from terminal
then either go to https://localhost:5000/render  or directly open template folder and click on index.html

workflow :
first the template for index.html . which is consist of a form tag includes an image upload button and 5 radio buttons representing a function .
functions : 
1>blurring
2>colourizing
3>sharpning
4>grayscaling
5>positive to negetive or vice versa.
after choosing respective image file and function click on submit button 
which submit the results under name variable through post method 
after saving the file and obtaining the filename the function then check for required function and redirect the file name to that function .
this function the read through imread process the work and save it through imwrite .
then render it to output.html 
then at output.html through jinja2 the image is processed image is shown in the site.
A download button is also placed under the picture using bootstrap to process the function of download through anchor tag .
