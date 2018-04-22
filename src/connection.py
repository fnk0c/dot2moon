#!/usr/bin/python
#coding: utf-8

__AUTHOR__ = "Fnkoc"
__LICENSE__= "MIT"

"""
MIT License

Copyright (c) 2017 Franco Colombino

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from urllib.request import urlopen, Request
from urllib import parse
from urllib.error import HTTPError, URLError

import http

class verify(object):
    #Global Variables
    def __init__(self, target_url, verbose, UserAgent, TimeOut):
        self.target_url = target_url
        self.verbose = verbose
        self.UserAgent = UserAgent
        self.TimeOut = TimeOut

    #Analyse URL and hecks if input is valid
    def url(self):
        if self.target_url[0:4] != "http":
            self.target_url = "http://%s" % self.target_url
        
            if self.verbose == True:
                print(" [!] New URL: %s" % self.target_url)

    def parameter(self, par):
        par_dic = {}
        par = par.split("&")
        for p in par:
            ps = p.split("=")
            par_dic[ps[0]] = ps[1]

        return(par_dic)
            
        
    #Check if server is trying to redirect us
    def redirect(self, check, parameter):
        #See if server tries to redirect in main page
        if check == True:
            #Function with injection parameters
            if parameter == True:
                _url = self.target_url.split("/")[2]
                _url = "http://" + _url
                
                if self.verbose == True:
                    print(" [+] Checking Redirection for: %s" % _url)
                else:
                    pass
            else:
                pass
            #If different User Agent is required
            if self.UserAgent != None:
                server_url = urlopen(Request(
                        _url,
                        headers={"User-Agent":self.UserAgent}),
                        timeout=self.TimeOut).geturl()

            #If not, the default will be used
            else:
                server_url = urlopen(
                        _url, timeout=self.TimeOut).geturl()

            #If redirect happens
            if server_url != _url:
                print(" [!] Server is redirecting us to:")
                print(" >>> %s\n" % server_url)
                follow = input(" Accept redirect [y/N]? ").lower()

                if follow == "y":
                    _url = _url.split("/")
                    n = server_url.split("/")
                    self.target_url = self.target_url.replace(
                            _url[0], n[0]).replace(_url[2], n[2])
                    print(" [!] New target acquired: %s" % self.target_url)
                else:
                    #Don't follow redirection
                    pass
            else:
                #No parameter. Just the DNS URL
                pass

            return(self.target_url)

        #Check == False 
        else:
            if self.UserAgent != None:
                #If different User Agent is required
                server_url = urlopen(Request(
                        self.target_url,
                        headers={"User-Agent":self.UserAgent}),
                        timeout=self.TimeOut).geturl()

                #If not, the default will be used
            else:
                server_url = urlopen(
                        self.target_url,
                        timeout=self.TimeOut).geturl()

            if server_url != self.target_url:
                check_redirect = "redirect"
            else:
                check_redirect = "no_redirect"

            return(self.target_url, server_url, check_redirect)

    #Retrieve HTTP code
    def HTTPcode(self, check):
        #Here we split the URL in order to test only the domain HTTP status
        #when needed. 
        _url = self.target_url.split("/")[2]
        _url = "http://" + _url
        
        try:
            #Check will only be used to determine if server is open and if its
            #address is valid.
            if check == True:
                #If we need to change the UserAgent
                if self.UserAgent != None:
                    request_code = urlopen(Request(
                            _url,
                            headers={"User-Agent":self.UserAgent}),
                            timeout=self.TimeOut).getcode()

                #If not, default will be used
                else:
                    request_code = urlopen(
                            _url,
                            timeout=self.TimeOut).getcode()
        
                return(self.target_url, request_code)

            else:
                #If different User Agent is required
                if self.UserAgent != None:
                    request_code = urlopen(Request(
                            self.target_url,
                            headers={"User-Agent":self.UserAgent}),
                            timeout=self.TimeOut).getcode()

                #If not, default will be used
                else:
                    request_code = urlopen(
                            self.target_url,
                            timeout=self.TimeOut).getcode()
       
                if self.verbose == True:
                    print(self.target_url, request_code)
                else:
                    pass
    
                return(self.target_url, request_code)

        except HTTPError as e:
            if self.verbose == True:    
                print(self.target_url, e.code)
            return(self.target_url, e.code)
        
        except URLError as e:
            if "timed out" in str(e):
                print(e)
                print(" [-] Server timed out. Try to increase timeout")

                #If fails on check then it will fail in every other test. Exit
                if check == True:
                    exit()
                #If not in check, pass to another payload
                else:
                    #Returns 504 (timeout)
                    return(self.target_url, 504)
            else:
                return(self.target_url, 404)

        except http.client.BadStatusLine as e:
            print(e)
        
    #Get page size in bytes
    def PageSize(self, check):
        #If different User Agent is required
        if check == True:
            try:
                if self.UserAgent != None:
                    page_size = len(urlopen(Request(
                            self.target_url + "a",
                            headers={"User-Agent":self.UserAgent}),
                            timeout=self.TimeOut).read())

                #If not, default will be used
                else:
                    page_size = len(urlopen(
                            self.target_url + "a",
                            timeout=self.TimeOut).read())

            except HTTPError as e:
                print(e)
                page_size = "Can't get default page size"
            
            if self.verbose == True:
                print(" [+] Default page size: %s bytes" % page_size)

        else:
            if self.UserAgent != None:
                page_size = len(urlopen(Request(
                        self.target_url,
                        headers={"User-Agent":self.UserAgent}),
                        timeout=self.TimeOut).read())

            #If not, default will be used
            else:
                page_size = len(urlopen(
                        self.target_url,
                        timeout=self.TimeOut).read())

            if self.verbose == True:
                print(self.target_url, page_size)
            
        return(self.target_url, page_size)

    def HTML(self, check):
        try:
            if self.UserAgent != None:
                page_html = urlopen(Request(
                        self.target_url,
                        headers={"User-Agent":self.UserAgent}),
                        timeout=self.TimeOut).read().decode("utf-8")

            #If not, the default will be used
            else:
                page_html = urlopen(
                        self.target_url,
                        timeout=self.TimeOut).read().decode("utf-8")

        except HTTPError:
            page_html = "Can't get page source code"

        if self.verbose == True:
            print(" [+] Source code got from %s" % self.target_url)
            print("----START" + "-"*71)
            print(page_html)
            print("----END" + "-"*73)

        return(page_html)

    def post(self, payload, request_par):
        data = parse.urlencode(request_par).encode()

        if self.UserAgent != None:
            req = Request(
                    self.target_url,
                    data=data, 
                    headers={"User-Agent":self.UserAgent})
            conn = urlopen(req, timeout=self.TimeOut)
        else:
            conn = urlopen(self.target_url,
                    data=data,
                    timeout=self.TimeOut)

        html = conn.read().decode("utf-8")
        page_size = len(html)

        if self.verbose == True:
            print(" [+] Source code got from %s" % payload)
            print("----START" + "-"*71)
            print(html)
            print("----END" + "-"*73)
        
        return(self.target_url, page_size, html, payload)

