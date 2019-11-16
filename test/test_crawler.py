import pytest
import json
import requests_mock
import os
from crawler import GithubWebSearch

DIR = os.path.dirname(__file__)

TESTS_HTTP_MAPPER ={
	'https://github.com/search?p=1&q=openstack+nova+css&type=Repositories': 'repos.html',
	'https://github.com/search?p=1&q=studio+guitar+gibson&type=Wikis': 'wikis.html',
	'https://github.com/search?p=1&q=ktarasz+terraform&type=Issues': 'issues.html',
	'https://github.com/michealbalogun/Horizon-dashboard': 'michealbalogun_Horizon-dashboard.html',
	'https://github.com/atuldjadhav/DropBox-Cloud-Storage': 'atuldjadhav_DropBox-Cloud-Storage.html'
}




def load_test_data(filename):
	with open(os.path.join(DIR, f'data/{filename}')) as fd:
		return fd.read()

def mock_http_pages(requests_mock, pages):
	for page in pages:
		requests_mock.get(
			page, text=load_test_data(TESTS_HTTP_MAPPER[page]), complete_qs=True
		)


def basic_test_template(requests_mock, crawler, results_data_filename, mock_urls):
	mock_http_pages(requests_mock, mock_urls)
	for batch in crawler:
		assert batch == json.loads(load_test_data(results_data_filename))


def test_repositories_without_extra(requests_mock):
	"""
	https://github.com/search?p=1&q=openstack+nova+css&type=Repositories
	"""
	crawler = GithubWebSearch(
		('openstack', 'nova', 'css'), 'Repositories',
		extra=False, proxies=('194.126.37.94:8080', '13.78.125.167:8080',)
	)
	basic_test_template(
		requests_mock,
		crawler,
		'repos.json',
		('https://github.com/search?p=1&q=openstack+nova+css&type=Repositories',),
	)


def test_issues_without_extra(requests_mock):
	"""
	Ref: https://github.com/search?p=1&q=ktarasz&type=Issues
	"""
	crawler = GithubWebSearch(
		('ktarasz', 'terraform'), 'Issues', extra=False,
		proxies=('194.126.37.94:8080', '13.78.125.167:8080',)
	)
	basic_test_template(
		requests_mock,
		crawler,
		'issues.json',
		('https://github.com/search?p=1&q=ktarasz+terraform&type=Issues',),
	)


#
def test_wikies_without_extra(requests_mock):
	"""
	Ref: https://github.com/search?p=1&q=studio+guitar+gibson&type=Wikis
	"""
	crawler = GithubWebSearch(
		('studio', 'guitar', 'gibson',), 'Wikis', extra=False,
		proxies=('194.126.37.94:8080', '13.78.125.167:8080',)
	)
	basic_test_template(
		requests_mock,
		crawler,
		'wikis.json',
		('https://github.com/search?p=1&q=studio+guitar+gibson&type=Wikis',),
	)


def test_repositories_with_extra(requests_mock):
	"""
	https://github.com/search?p=1&q=openstack+nova+css&type=Repositories
	"""
	crawler = GithubWebSearch(
		('openstack', 'nova', 'css'), 'Repositories',
		extra=True, proxies=('194.126.37.94:8080', '13.78.125.167:8080',)
	)
	basic_test_template(
		requests_mock,
		crawler,
		'repos_w_extra.json',
		(
			'https://github.com/search?p=1&q=openstack+nova+css&type=Repositories',
			'https://github.com/michealbalogun/Horizon-dashboard',
			'https://github.com/atuldjadhav/DropBox-Cloud-Storage',
		),
	)
