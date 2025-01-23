from pydantic import (
    BaseModel,
    StringConstraints,
    Field,
    model_validator,
    field_validator,
)

from typing_extensions import Annotated
from typing import List
from enum import Enum
from datetime import datetime


class ShowTypes(str, Enum):
    MOVIE = "Movie"
    TVSHOW = "TV Show"

    def __str__(self):
        return self.value


constr_str = Annotated[str | None, StringConstraints(min_length=3, max_length=50)]


class ShowSearchFilter(BaseModel):
    type: ShowTypes | None = Field(None)
    title: constr_str = None
    director: List[constr_str] | None = Field(None, min_length=1, max_length=10)
    rating: Annotated[str | None, StringConstraints(min_length=1, max_length=10)] = None
    cast: List[constr_str] | None = Field(None, min_length=1, max_length=10)
    country: List[constr_str] | None = Field(None, min_length=1, max_length=10)
    date_added: datetime | None = None
    release_year: int | None = Field(None, ge=1900, le=2025)
    duration: Annotated[str | None, StringConstraints(min_length=3, max_length=10)] = (
        None
    )
    listed_in: List[constr_str] | None = Field(None, min_length=1, max_length=10)
    description: constr_str = None

    @model_validator(mode="before")
    def validate_at_least_one_field(cls, values):
        search_fields = [
            "type",
            "title",
            "director",
            "rating",
            "cast",
            "country",
            "date_added",
            "release_year",
            "duration",
            "listed_in",
            "description",
        ]

        if not any(values.get(field) for field in search_fields):
            raise ValueError(
                f"At least one search field must be provided. "
                f"Search fields are: {', '.join(search_fields)}"
            )
        return values

    @field_validator("director", "cast", "country", "listed_in", mode="before")
    @classmethod
    def convert_to_list(cls, v):
        if v is None:
            return None
        return [v] if not isinstance(v, list) else v

    @field_validator("type", mode="before")
    def validate_type_case_insensitive(cls, v):
        if v is None:
            return None

        normalized = v.lower().replace(" ", "")
        for member in ShowTypes:
            if member.value.lower().replace(" ", "") == normalized:
                return member

        raise ValueError(f"Invalid show type: {v}")


class ShowSearchInput(ShowSearchFilter):
    limit: int = Field(10, gt=0, le=10)
    offset: int = 0


class LogInput(BaseModel):
    username: Annotated[str, StringConstraints(min_length=1, max_length=20)]
    password: Annotated[str, StringConstraints(min_length=1, max_length=50)]
