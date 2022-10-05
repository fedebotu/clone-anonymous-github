XXXX-1 XXXX-2
================

XXXX-1 XXXX-2 is a system to anonymize XXXX-2 repositories before referring to them in a double-XXXX-1 paper submission.
To start using XXXX-1 XXXX-2 right now: **[XXXX-1](XXXX-1)**

Indeed, in a double-XXXX-1 review process, the open-science data or code that is in the online appendix must be anonymized, similarly to paper anonymization. The authors must

* anonymize URLs: the name of the institution/department/group/authors should not appear in the  URLs of the open-science appendix
* anonymize the appendix content itself

Anonymizing an open-science appendix needs some work, but fortunately, this can be automated, this is what XXXX-1 XXXX-2 is about.

XXXX-1 XXXX-2 anonymizes:
* the XXXX-2 owner / organization / repository name
* the content of the repository
  * file contents (all extensions, md/txt/java/etc)
  * file and directory names

Question / Feedback / Bug report: please open an issue in this repository.

Using XXXX-1 XXXX-2
-----------------------


## How to create a new anonymized repository

To use it, open the main page (e.g., [XXXX-1](XXXX-1)), login with XXXX-2, and click on "Anonymize".
Simply fill 1. the XXXX-2 repo URL and 2. the id of the anonymized repository, 3. the terms to anonymize (which can be updated afterward). 
The anonymization of the content is done by replacing all occurrences of words in a list by "XXXX" (can be changed in the configuration). 
The word list is provided by the authors, and typically contains the institution name, author names, logins, etc...
The README is anonymized as well as all files of the repository. Even filenames are anonymized. 

In a paper under double-XXXX-1 review, instead of putting a link to XXXX-2, one puts a link to the XXXX-1 XXXX-2 instance (e.g. 
XXXX-1 which is an XXXX-1 version of this repo).

To start using XXXX-1 XXXX-2 right now, a public instance of anonymous_github is hosted at 4open.science:

**[XXXX-1](XXXX-1)**

## What is the scope of anonymization?

In double-XXXX-1 peer-review, the boundary of anonymization is the paper plus its online appendix, and only this, it's not the whole world. Googling any part of the paper or the online appendix can be considered as a deliberate attempt to break anonymity ([explanation](XXXX-1))


How does it work?
-----------------

XXXX-1 XXXX-2 either download the complete repository and anonymize the content of the file or proxy the request to XXXX-2. In both case, the original and anonymized versions of the file are cached on the server. 

Installing XXXX-1 XXXX-2
----------------------------
1. Clone the repository
```bash
git clone https://b10200cbde7d/r/840c8c57-3c32-451e-bf12-0e20be300389/
cd anonymous_github
npm i
```

2. Configure the XXXX-2 token

Create a file `.env` that contains

```env
GITHUB_TOKEN=<GITHUB_TOKEN>
CLIENT_ID=<CLIENT_ID>
CLIENT_SECRET=<CLIENT_SECRET>
PORT=5000
DB_USERNAME=
DB_PASSWORD=
AUTH_CALLBACK=XXXX-2,
```

`GITHUB_TOKEN` can be generated here: XXXX-2 with `repo` scope.
`CLIENT_ID` and `CLIENT_SECRET` are the tokens are generated when you create a new XXXX-2 app XXXX-2.
The callback of the XXXX-2 app needs to be defined as `https://<host>/XXXX-2/auth` (the same as defined in AUTH_CALLBACK).

3. Run XXXX-1 XXXX-2
```bash
docker-compose up -d
```

4. Go to XXXX-1 XXXX-2

By default, XXXX-1 XXXX-2 uses port 5000. It can be changed in `docker-compose.yml`.


Related tools
--------------
[gitmask](https://www.gitmask.com/) is a tool to anonymously contribute to a XXXX-2 repository.

[blind-reviews](XXXX-2) is a browser add-on that enables a person reviewing a XXXX-2 pull request to hide identifying information about the person submitting it.

See also
--------

* [Open-science and double-XXXX-1 Peer-Review](XXXX-1)
