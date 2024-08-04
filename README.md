TARUMT ITP Scraper
==================

A utility tool to scrape job listings from TARUMT ITP site, allowing easy data searching and filtering through all the listings.

Usage
-----

Example:

```python
import tar_itp_scraper as itp

for job_listing in itp.get_full_job_listings():
    if "python" in job_listing.job_description.casefold():
        print(job_listing.pretty)
        print('=' * 100)
        print()
```