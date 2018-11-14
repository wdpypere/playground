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
        if not repo['archived']:
            repolist.append(repo['name'])

    return repolist


def printpullrequests(prlist, name):
    """
    Pretty print a list of pullrequests per repo.
    """
    reposc = 0
    prsc = 0

    for repo in sorted(prlist.iterkeys()):
        if not "easybuild" in repo and not "easyblocks_ugent" in repo:
            reposc += 1
            for prq in prlist[repo]:
                prsc += 1

    print '--------------------------------------------'
    print " %s PR's in %s repositories. (%s)" % (prsc, reposc, name)
    print '--------------------------------------------'

    for repo in sorted(prlist.iterkeys()):
        if not "easybuild" in repo and not "easyblocks_ugent" in repo:
            print repo
            reposc += 1
            for prq in prlist[repo]:
                prsc += 1
                title = prq['title'].encode('utf-8')
                user = prq['user'].encode('utf-8')
                dates = prq['cdate'].encode('utf-8')
                urls = prq['url'].encode('utf-8')
                print " - %s by %s at %s - %s" % (title, user, dates, urls)

    print '\n'

def main():
    """
    Main logic of the script.
    """
    repolistgh = getallrepos(GHREPOURL, GHTOKEN)
    repolistug = getallrepos(UGREPOURL, UGTOKEN)
    prlistgh = getpullrequests(repolistgh, GHREPOBASEURL, GHTOKEN)
    prlistug = getpullrequests(repolistug, UGREPOBASEURL, UGTOKEN)
    printpullrequests(prlistug, 'github.ugent.be')
    printpullrequests(prlistgh, 'github.com')

    print '--------------------------------------------'
    print "Don't forget that you can see your pull requests, mentions, issues, ... at:"
    print " - https://github.com/pulls"
    print " - https://github.com/issues"
    print " - https://github.ugent.be/pulls"
    print " - https://github.ugent.be/issues"


if __name__ == "__main__":
    main()
