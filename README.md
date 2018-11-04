# gcrawl
Google Terminal Client

Google Terminal Client brings the Google Search to the terminal. It gives the user the search results without even opening the browser in a much faster way. Users with help of google may be able to search one group of words at a time but with this we are able to fetch results for multiple searches at the same time. All of this is done using parallel processing which makes the processes even faster. 

The Google Terminal Client can also be used with a distributed nodes which makes the process much faster. 
The project uses the flexibility of python language and gearman for the distributed framework.



gsearch() algorithm:

1.  Program uses the Google Search to generate a list of all the links related to the search.
2.  Later the program reads and fetches the titles of each html pages that the links and prints it to the terminal.
    This on the single node is done using python's multiprocessing library.

