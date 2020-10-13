# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for
import dns.message
import dns.query
import dns.flags


def my_dns_query(hostname, query_type, recrusion_desire, server):
    query = dns.message.make_query(hostname, query_type)

    if(not recrusion_desire):
        query.flags ^= dns.flags.RD

    query_response = dns.query.udp(query, server)
    print(query_response)

    # for k in query_response.answer:
    # 	print("........")
    # 	for u in k.items:
    # 		print(u)
    # 	print("........")

    return query_response.to_text()

# my_dns_query("iitjammu.ac.in","CNAME",True,"192.168.43.1")


# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

# Flask constructor takes the name of
# current module (__name__) as argument.
# app = Flask(__name__, template_folder="template")
app = Flask(__name__, template_folder="templates", static_folder="static")


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.


@app.route("/")
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return render_template("index.html", params=["www.google.com", "8.8.8.8", ["checked", "", "", "", "",
                                                                               "", "", "", "", "", ""], "checked"], answer="")


@app.route('/favicon.ico/', methods=['GET', ])
def favicon():
    # """This function handles when a user uses a web browser to access the LG directly."""
    return app.send_static_file("favicon.ico")


@app.route("/search")
def search():
    hostname = request.args.get('hostname')
    query_type = request.args.get('query_type')
    recrusion_desire = request.args.get('rd')
    if(recrusion_desire == "on"):
        rd = True
    else:
        rd = False

    server = request.args.get("server")
    lis = ["A", "AAAA", "MX", "ANY", "CNAME",
           "CAA", "NS", "PTR", "SOA", "SRV", "TXT"]

    send_list = [""for x in range(len(lis))]
    send_list[lis.index(query_type)] = "checked"
    print(send_list)

    if(recrusion_desire == "on"):
        rd1 = "checked"
    else:
        rd1 = ""
    return render_template("index.html", params=[hostname, server, send_list, rd1], answer=my_dns_query(hostname, query_type, rd, server))

    # return "%s!" % my_dns_query(hostname,query_type,rd,server)
# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host="0.0.0.0", port=5003)
