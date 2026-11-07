import arxiv 

def search_arxiv(query:str , max_results : int = 10):

	results = []

	try:

		client = arxiv.Client()

		search = arxiv.Search( query = query  , max_results = max_results , sort_by = arxiv.SortCriterion.Relevance)

		papers = client.results(search)

		for paper in papers :

			results.append({
				"title": paper.title,

				"url" : paper.entry_id  , 

				"snippet" : paper.summary , 

				"source_type" : "arxiv" , 

				"authors" : [author.name for author in paper.authors],

				"published_date" : (paper.published.isoformat()) , 

				"pdf_url" : paper.pdf_url
				})

	except Exception as e :
		print(f" arxiv search error : {e}")
	return results 

