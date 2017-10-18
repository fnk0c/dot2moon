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

#Class responsible to analyse HTML content
class crawler(object):
    def __init__(self, html, verbose):
        self.html = html
        self.verbose = verbose

    #Verify if HTML contains determinated payload name
    def payload(self, target):
        url = target.split("=")
        test = len(url)
        test = url[test-1]
        test = test.split("/")
        string = len(test)
        string = test[string-1]

        #Check if string is in HTML
        if string in self.html:
            return("found")
        #If not, it might contain useful information
        else:
           return(target, self.html, "not_found")

    #Verify if HTML contains determinated strings
    def strings(self, specific):
        string = [
                "not found", "not be found", " Not Found", "nao encontrado",
                "não encontrado", "Página no Encontrada"]

        if specific != None:
            string.append(specific)
        else:
            pass

        #Go through all the list
        for i in string:
            #If the string is found
            if i in self.html:
                if self.verbose == True:
                    print(\
                    "string \"%s\" detected inside source code. Discarting" % i)
                else:
                    pass
                status = "found"
                break
            else:
                status = "not_found"
        
        return(status)

    #Verify if Source code has changed between default page and now
    def compare(self, default):
        if default == self.html:
            if self.verbose == True:
                print("Source code has not changed. Discarting")
            return("equal")
        else:
            return("not_equal")
