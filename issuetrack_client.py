# Isabel Ojeda
# HW7 Q2

from requests.auth import HTTPBasicAuth
import requests
import csv
from collections import defaultdict
URL = "http://jcssdev.pythonanywhere.com/"
bugs = []
comments = []

# parses the list of bugs
def parse_bugs(bugs, csv_writer):	
	for b in bugs:
		csv_writer.writerow([b["id"], b["package"], b["status"], b["summary"]])
	
# parses the list of bugs
def parse_comments(comments, csv_writer):	
	for c in comments:
		csv_writer.writerow([c["id"], c["bug"], c["user"], c["content"]])

def visit_url(resource, callback):
	# open file
	with open(f"{resource}.csv", "w", newline='', encoding="utf8") as csvfile:
		csv_writer = csv.writer(csvfile, delimiter=',',quotechar='"')
		csv_writer.writerow(["id","package","status","summary"])

		# composes request URL
		url = URL + resource
		# while the `next` page to visit is not None
		while url:
			print(url)
			# HTTP request without authentication
			response = requests.get(url)
			if response:
				# parse the response to JSON
				json_resp = response.json()
				# get the next page
				url = json_resp["next"] 
				# parse the returned user information
				callback(json_resp["results"], csv_writer)
			else:
				url = None

# csv file
def bugs_per_package(bugs): 
    count = defaultdict(int)
    for bug in bugs:
        package = bug["package"]
        count[package] += 1
    with open("total_bugs_per_package.csv", "w") as f:
        csv_writer = csv.writer(f, delimiter=",", quotechar="'") # create writer object
        csv_writer.writerow(["package", "bugs"]) # header row
        for package, count in count.items():
            csv_writer.writerow([package, count]) # write each pair in one row

# csv file
def comments_per_bug(comments): 
	count = defaultdict(int)
	for comment in comments:
		bug = comment["bug"]
		id = int(bug.strip("/").split('/')[-1])
		count[id] += 1
	with open("total_comments_per_bug.csv", "w") as f:
		csv_writer = csv.writer(f, delimiter=",", quotechar="'")
		csv_writer.writerow(["bug_id", "total"])
		for id, count in count.items(): 
			csv_writer.writerow([id, count])

# get the data from bugs file
def get_bugs_per_package(bugs_list, _):
	bugs.extend(bugs_list)

# get the dara from comments file 
def get_comments_per_bug(comments_list, _):
	comments.extend(comments_list)
		             

def main():
	# write csv files raw data, but does not return anything 
	visit_url("bugs", parse_bugs)
	visit_url("comments", parse_comments)

	# put csv info into lists
	visit_url("bugs", get_bugs_per_package)
	visit_url("comments", get_comments_per_bug)
	
	# write csv files using lists 
	bugs_per_package(bugs)
	comments_per_bug(comments)
	


if __name__ == '__main__':
	main()