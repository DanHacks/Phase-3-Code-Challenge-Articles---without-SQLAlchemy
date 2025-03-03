# Deliverables
# Write the following methods in the classes in the files provided. Feel free to build out any helper methods if needed.

# Remember: SQLAlchemy gives your classes access to a lot of methods already! Keep in mind what methods SQLAlchemy gives you access to on each of your classes when you're approaching the deliverables below.

# Migrations
# Before working on the rest of the deliverables, you will need to create a migration for the freebies table.

# A Freebie belongs to a Dev, and a Freebie also belongs to a Company. In your migration, create any columns your freebies table will need to establish these relationships using the right foreign keys.
# The freebies table should also have:
# An item_name column that stores a string.
# A value column that stores an integer.
# After creating the freebies table using a migration, use the seed.py file to create instances of your Freebie class so you can test your code.

# After you've set up your freebies table, work on building out the following deliverables.

# Relationship Attributes and Methods
# Use SQLAlchemy's ForeignKey, relationship(), and backref() objects to build relationships between your three models.

# Note: The plural of "freebie" is "freebies" and the singular of "freebies" is "freebie".

# Freebie
# Freebie.dev returns the Dev instance for this Freebie.
# Freebie.company returns the Company instance for this Freebie.
# Company
# Company.freebies returns a collection of all the freebies for the Company.
# Company.devs returns a collection of all the devs who collected freebies from the company.
# Dev
# Dev.freebies returns a collection of all the freebies that the Dev has collected.
# Dev.companiesreturns a collection of all the companies that the Dev has collected freebies from.
# Use python debug.py and check that these methods work before proceeding. For example, you should be able to retrieve a dev from the database by its attributes and view their companies with dev.companies (based on your seed data).

# Aggregate Methods
# Freebie
# Freebie.print_details()should return a string formatted as follows: {dev name} owns a {freebie item_name} from {company name}.
# Company
# Company.give_freebie(dev, item_name, value) takes a dev (an instance of the Dev class), an item_name (string), and a value as arguments, and creates a new Freebie instance associated with this company and the given dev.
# Class method Company.oldest_company()returns the Company instance with the earliest founding year.
# Dev
# Dev.received_one(item_name) accepts an item_name (string) and returns True if any of the freebies associated with the dev has that item_name, otherwise returns False.
# Dev.give_away(dev, freebie) accepts a Dev instance and a Freebie instance, changes the freebie's dev to be the given dev; your code should only make the change if the freebie belongs to the dev who's giving it away

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base


Base = declarative_base()
engine = create_engine("sqlite:///freebies.db")
Session = sessionmaker(bind=engine)
session = Session()

# here we have the many to many association table of companies and devs
devs_companies = Table(
    "devs_companies",
    Base.metadata,
    Column("dev_id", Integer, ForeignKey("devs.id")),
    Column("company_id", Integer, ForeignKey("companies.id"))
)




class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    founding_year = Column(Integer, nullable=False)

    # here we now explain the relationship of freebies and devs
    freebies = relationship("Freebie", back_populates="company", cascade="all, delete-orphan")
    devs = relationship("Dev", secondary=devs_companies, back_populates="companies")
    
    # here we give a free freebie to a dev
    def give_freebie(self, dev, item_name,value):
        freebie = Freebie(item_name=item_name, value=value, company=self, dev=dev)
        session.add(freebie)
        session.commit()

    # here we find the oldest company
    @classmethod
    def oldest_company(cls):
        return session.query(Company).order_by(Company.founding_year).first()
    

class Dev(Base):
    __tablename__ = "devs"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # here we now explain the relationship to freebies and companies
    freebies = relationship("Freebie", back_populates="dev")
    companies = relationship("Company", secondary=devs_companies, back_populates="devs")

    # here we check if a dev has received a certain item
    def received_one(self, item_name):
        return session.query(Freebie).filter(Freebie.dev_id == self.id, Freebie.item_name == item_name).first() is not None
    # here we change the dev who a freebie belongs to
    def give_out(self, dev, freebie):
        if not isinstance(dev, Dev):
            raise TypeError("Recepient must be a valid Dev instance")
        if freebie.dev != self:
            raise ValueError("Freebie does not belong to the current dev")
        freebie.dev = dev
        session.commit()
        return True

      
    
    # here we return only the company which a dev has received freebies
    @property
    def companies_with_freebies(self):
        return {freebie.company for freebie in self.freebies}


    

class Freebie(Base):
    __tablename__ = "freebies"
    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    dev_id = Column(Integer, ForeignKey("devs.id"), nullable=False)

    # here we now explain the relationship to companies and devs
    company = relationship("Company", back_populates="freebies")
    dev = relationship("Dev", back_populates="freebies")

    # here we check if a freebie belongs to a certain dev
    def belongs_to(self, dev):
        return self.dev == dev

    # here we print the details of a freebie
    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}."
    

Base.metadata.create_all(engine)
    

