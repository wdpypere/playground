#!/usr/bin/python
'''
Created on Aug 04, 2014

@author: wdpypere
'''
import datetime
import requests
import json
import sys

GHREPOURL = 'https://api.github.com/orgs/hpcugent/repos'
GHREPOBASEURL = 'https://api.github.com/repos/hpcugent'
GHTOKEN = ''

UGTOKEN = ''
UGREPOURL = 'https://github.ugent.be/api/v3/orgs/hpcugent/repos'
UGREPOBASEURL = 'https://github.ugent.be/api/v3/repos/hpcugent'


def dorequest(link, token):
    """
    Fetch data using requests and token.
    """
    link += "?access_token=" + token + "&per_page=300"
    result = requests.get(link)
    if result.status_code == requests.codes.ok:
        return result

    else:
        print "Something went wrong, got http resonse %s, when trying %s." % (result.status_code, link)
        sys.exit(1)

def getpullrequests(repolist, baseurl, token):
    """
    Get the list of pull requests per repo. Return a list of the open ones with:
     - name
     - link
     - creation date
     - user
    """
    newlist = {}
    for repo in repolist:
        link = '%s/%s/pulls' % (baseurl, repo)
        result = dorequest(link, token)
        for pullr in json.loads(result.text):

            if pullr['state'] == 'open':

                if repo not in newlist:
                    newlist[repo] = []

                plr = {}
                plr['title'] = pullr['title']
                plr['user'] = pullr['user']['login']
                plr['cdate'] = datetime.datetime.strptime(pullr['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime('%c')
                plr['url'] = pullr['html_url']
                newlist[repo].append(plr)

    return newlist


def getallrepos(repourl, token):
    """
    Fetch all the repos and return their names.
    """
    repolist = []
    result = dorequest(repourl, token)
    for repo in json.loads(result.text):
        repolist.append(repo['name'])

    return repolist


def printpullrequests(prlist):
    """
    Pretty print a list of pullrequests per repo.
    """
    for repo in sorted(prlist.iterkeys()):
        print repo
        for prq in prlist[repo]:
            print " - %s by %s at %s - %s" % (prq['title'], prq['user'], prq['cdate'], prq['url'])

        print "\n"


def main():
    """
    Main logic of the script.
    """
    repolistgh = getallrepos(GHREPOURL, GHTOKEN)
    repolistug = getallrepos(UGREPOURL, UGTOKEN)
    prlistgh = getpullrequests(repolistgh, GHREPOBASEURL, GHTOKEN)
    prlistug = getpullrequests(repolistug, UGREPOBASEURL, UGTOKEN)
    printpullrequests(prlistug)
    printpullrequests(prlistgh)


if __name__ == "__main__":
    main()
