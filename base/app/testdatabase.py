import requests
import json

base_url = "http://127.0.0.1:5000"
addcourse_url = "{}/addcourse".format(base_url)
addmac_url = "{}/updateMAC".format(base_url)

#test the updating of course
new_course = {
    "course_code" : "SMT203",
    "group_number" : "G1",
    "emails" : [
        "daryl@gmail.com",
        "hcboon@yahoo.com",
        "paul@tinder.com",
        "job@church.com"
    ],
    "names" : [
        "Daryl Ang",
        "Boon Hui Chiann",
        "Paul Cheong",
        "Job Seow"
    ],
    "start_time" : "1200",
    "end_time" : "1515",
    "location" : "SIS SR2-3"
}

r = requests.post(addcourse_url,new_course)
############################################

#test updating of mac
macs = {
    "emails" : [
        "daryl@gmail.com",
        "hcboon@yahoo.com",
        "paul@tinder.com",
        "job@church.com"
    ],
    "mac_adds" : [
        "daryl_mac",
        "hc_mac",
        "paul_mac",
        "job_mac"
    ]
}

for i in range(len(macs["emails"])):
    new_email = macs["emails"][i]
    new_mac = macs["mac_adds"][i]
    new_pair = {new_email:new_mac}
    r = requests.post(addmac_url,new_pair)
##############################################