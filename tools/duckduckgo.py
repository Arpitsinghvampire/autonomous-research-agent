from ddgs import DDGS  

def search_web(query : str, max_results :int = 10 ):

	results = []

	try:

		with DDGS() as ddgs:

			search_results = ddgs.text(query , max_results = max_results)

			for item in search_results :

				results.append({
					"title" : item.get("title" , ""),

					"url" : item.get("href" , ""),

					"snippet" : item.get("body" , ""),

					"source_type" : "web"

					})

	except Exception as e :

		print(f" DuckDuckgo search error is : {e}")

	return results 