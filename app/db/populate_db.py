import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from app.config import settings
from app.db.models import Base, Show
from app.db.crud import create_user


def split_column_data(df, column_name):
    df[column_name] = df[column_name].apply(
        lambda x: [] if pd.isna(x) else x.split(", ")
    )
    return df


def populate_db() -> None:
    df = pd.read_csv("/app/data/netflix.csv")
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")

    df = split_column_data(df, "cast")
    df = split_column_data(df, "country")
    df = split_column_data(df, "listed_in")
    df = split_column_data(df, "director")

    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    for _, row in df.iterrows():
        try:
            movie = Show(
                show_id=row["show_id"],
                type=row["type"],
                title=row["title"],
                director=row["director"],
                cast=row["cast"],
                country=row["country"],
                date_added=row["date_added"] if pd.notna(row["date_added"]) else None,
                release_year=int(row["release_year"])
                if pd.notna(row["release_year"])
                else None,
                rating=row["rating"],
                duration=row["duration"],
                listed_in=row["listed_in"],
                description=row["description"],
            )
            session.add(movie)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error processing row: {row['show_id']}")
            print(f"Error: {str(e)}")
    create_user(
        session=session,
        username=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
    )
    session.close()


if __name__ == "__main__":
    populate_db()
