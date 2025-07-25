### hello

### main.py

inside, main,
call a function that scrapes

### scrape.py

loops through to get all the links for each task page,
hand the url for each task page into a function called scrape_task_links,
get the returned links (as a list) and pass into a function called scrape_task_info,

### scrape_task_links(url)

goes throught the document and gets all the task links, puts into a list and returns it

### scrape_task_info(url)

gets the task url as an inpu and goes through the document and gets the task info,
puts into mongodb
