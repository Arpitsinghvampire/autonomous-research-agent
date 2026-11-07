from typing import Optional , List  
from pydantic import BaseModel , HttpUrl 


class ResearchSource(BaseModel):

	title : str  

	url : str 

	source_type : str 

	snippet : Optional[str] = None 

	content : Optional[str] = None 

	authors : List[str]  = []

	published_date : Optional[str] = None 

	relevance_score : Optional[str] = None 


class ResearchOutput(BaseModel):

	original_question : str 

	search_queries : List[str]

	sources : List[ResearchSource]

	total_sources : int  