from pydantic import (
    BaseModel,
    StringConstraints,
    Field,
    model_validator,
    field_validator,
)

from typing_extensions import Annotated
from typing import List


constr_str = Annotated[str | None, StringConstraints(min_length=3, max_length=50)]


class ShowSearchFilter(BaseModel):
    title: constr_str = None
    director: List[constr_str] | None = Field(None, min_length=3, max_length=10)
    rating: Annotated[str | None, StringConstraints(min_length=1, max_length=10)] = None
    cast: List[constr_str] | None = Field(None, min_length=3, max_length=10)
    country: List[constr_str] | None = Field(None, min_length=4, max_length=10)
    release_year: int | None = Field(None, ge=1900, le=2025)
    duration: Annotated[str | None, StringConstraints(min_length=3, max_length=10)] = (
        None
    )
    listed_in: List[constr_str] | None = Field(None, min_length=1, max_length=10)
    description: constr_str = None

    @model_validator(mode="before")
    def validate_at_least_one_field(cls, values):
        search_fields = [
            "title",
            "director",
            "rating",
            "cast",
            "country",
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


class ShowSearchInput(ShowSearchFilter):
    limit: int = Field(10, gt=0, le=10)
    offset: int = 0
