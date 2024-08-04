from .job_listing import JobListing, JobFullListing
from .constants.states import States
from .constants.job_category import JobCategory
from .utils import Range

import requests
import urllib3
from typing import Iterable
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter


__all__ = (
    "get_job_listings",
    "get_full_job_listings",
    "resolve_job_listing"
)


ENDPOINT = "https://itp.tarc.edu.my"
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)


def get_job_listings(
        *,
        company_name: str = "",
        job_title: str = "",
        state: States = None,
        salary_range: Range = Range(300, 3000),
        job_categories: tuple[JobCategory, ...] = ()
) -> Iterable[JobListing]:
    payload = {
        "company": company_name,
        "jobTitle": job_title,
        "state": state,
        "salaryMin": salary_range.min,
        "salaryMax": salary_range.max
    }
    if job_categories:
        payload["jobCat[]"] = [job.value for job in job_categories]

    ret = requests.post(ENDPOINT + "/filter-job", verify=False)
    ret.raise_for_status()

    for listing in ret.json()["list"]:
        yield JobListing.map_from_json(listing)


def resolve_job_listing(job_listing: JobListing) -> JobFullListing:
    ret = requests.get(job_listing.full_listing_url, verify=False)
    ret.raise_for_status()

    soup = BeautifulSoup(ret.content, "lxml")
    body = soup\
        .find(class_="card-body")\
        .find(class_="row")
    description, infobox = body\
        .find_all("div", recursive=False)

    infobox = infobox.find("table")
    working_day = infobox.find_all("tr")[2].find("td")
    working_hour = infobox.find_all("tr")[3].find("td")
    provided_accessory = infobox.find_all("tr")[6].find("td")
    accommodation = infobox.find_all("tr")[7].find("td")

    return JobFullListing(
        job_title=job_listing.job_title,
        salary_range=job_listing.salary_range,
        address=job_listing.address,
        company_name=job_listing.company_name,
        company_logo_url=job_listing.company_logo_url,
        posted_at=job_listing.posted_at,
        qualification=job_listing.qualification,
        full_listing_url=job_listing.full_listing_url,
        job_description=MarkdownConverter().convert_soup(description).strip("\n"),
        working_day=working_day.get_text(strip=True),
        working_hour=working_hour.get_text(strip=True),
        provided_accessory=provided_accessory.get_text(strip=True),
        accommodation=True if accommodation.get_text(strip=True) != "No" else False,
    )


def get_full_job_listings(
        *,
        company_name: str = "",
        job_title: str = "",
        state: States = None,
        salary_range: Range = Range(300, 3000),
        job_categories: tuple[JobCategory, ...] = ()
) -> Iterable[JobFullListing]:
    for job_listing in get_job_listings(
            company_name=company_name,
            job_title=job_title,
            state=state,
            salary_range=salary_range,
            job_categories=job_categories):
        yield resolve_job_listing(job_listing)
