from .utils import Range, strtol
from .constants.qualification import Qualification

from attrs import define
from datetime import datetime, timedelta
from typing import Self

__all__ = (
    "JobListing",
    "JobFullListing"
)


@define
class JobListing:
    job_title: str
    salary_range: Range

    address: str
    company_name: str
    company_logo_url: str

    posted_at: datetime
    qualification: Qualification

    full_listing_url: str

    @property
    def pretty(self) -> str:
        return \
            f"Job Title: {self.job_title}\n" \
            f"Salary: RM{self.salary_range.min} - RM{self.salary_range.max}\n" \
            f"Url: {self.full_listing_url}\n" \
            "\n" \
            f"Company: {self.company_name}\n" \
            f"Address: {self.address}\n" \
            "\n" \
            f"Posted at: {self.posted_at}\n" \
            "\n" \
            f"Qualifications Required: {self.qualification}\n"

    @classmethod
    def map_from_json(cls, json: dict) -> Self:
        def get_address(address: str) -> str:
            return address.replace(",,", ",")

        def get_qualification(qualifications: str) -> Qualification:
            qualifications = qualifications.casefold()
            qualification: Qualification = Qualification.NONE

            if "diploma" in qualifications:
                qualification |= Qualification.DIPLOMA
            if "degree" in qualifications:
                qualification |= Qualification.DEGREE

            return qualification

        def get_posted_at(timestamp: str) -> datetime:
            now = datetime.now()

            if "minute" in timestamp:  # not confirmed, just speculation
                return now - timedelta(minutes=strtol(timestamp)[0])
            if "hour" in timestamp:
                return now - timedelta(hours=strtol(timestamp)[0])
            if "day" in timestamp:
                return now - timedelta(days=strtol(timestamp)[0])
            if "month" in timestamp:
                return now - timedelta(days=strtol(timestamp)[0] * 30)
            if "year" in timestamp:
                return now - timedelta(days=strtol(timestamp)[0] * 365)

            return now

        return cls(
            job_title=json["title"],
            salary_range=Range(
                float(json["minSalary"].replace(",", "")),
                float(json["maxSalary"].replace(",", ""))
            ),
            address=get_address(json["addr"]),
            company_name=json["compName"],
            company_logo_url=f"https://itp.tarc.edu.my/storage/company/logo{json["compLogo"]}",
            posted_at=get_posted_at(json["postAt"]),
            qualification=get_qualification(json["qualification"]),
            full_listing_url=json["route"]
        )


@define
class JobFullListing(JobListing):
    job_description: str

    working_day: str
    working_hour: str
    provided_accessory: str
    accommodation: bool

    @property
    def pretty(self) -> str:
        return super().pretty + "\n" \
            f"Working Day: {self.working_day} ({self.working_hour})\n" \
            "\n" \
            f"Provided: {self.provided_accessory}\n" \
            f"Accommodation: {"Yes" if self.accommodation else "No"}\n" \
            "\n" \
            "Job Description:\n" \
            f"{self.job_description}\n"
