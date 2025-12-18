from pydantic import BaseModel,Field

class File(BaseModel):
    path: str = Field(description="The path to the file to be created or modified")
    purpose: str = Field(description="The purpose of the file, eg. 'main application logic', 'data processing module', etc.")

class Plan(BaseModel):
    name: str = Field(description="The name of app to be built")
    description: str = Field(description="A oneline description of the app to be built, eg. 'A web application for managing personal finances'")
    techstack: str = Field(description="The tech stack to be used for the app. eg. 'python', 'javascript', 'react', 'flask', etc.")
    features: list[str] = Field(description="A list of features that the app should have. eg. 'user authentication', 'data visualization', etc.")
    files: list[File] = Field(description="A list of files to be created, each with a 'path' and 'purpose'")