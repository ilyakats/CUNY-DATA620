library(XML)
library(RCurl)
library(dplyr)
library(tidyr)
library(stringr)

yankees_ws <- c(1923, 1927, 1928, 1932, 1936, 1937, 1938, 1939, 1941, 1943,
                1947, 1949, 1950, 1951, 1952, 1953, 1956, 1958, 1961, 1962,
                1977, 1978, 1996, 1998, 1999, 2000, 2009)

all_yanks <- data.frame(Name = character(), Year = integer())

for(i in 1:length(yankees_ws)) {
  url <- getURL(str_c("http://www.baseball-reference.com/teams/NYY/",yankees_ws[i],"-roster.shtml"))
  tmp <- readHTMLTable(url, which = 1)
  tmp <- mutate(tmp[1], Year = yankees_ws[i])
  all_yanks <- rbind(all_yanks, tmp)
}

edges <- all_yanks %>% 
  inner_join(all_yanks, all_yanks, by = "Year") %>% 
  filter(Name.x != Name.y) %>% 
  select(Player1 = Name.x, Player2 = Name.y)
edges <- unique(edges[,1:2])

for(i in 1:nrow(edges)) {
  if (as.character(edges[i,1]) < as.character(edges[i,2])) {
    edges[i,] <- select(edges[i,], Player1 = Player2, Player2 = Player1)
  }
}
edges <- unique(edges[,1:2])
nodes <- unique(all_yanks[1])

write.csv(nodes, file = "nodes.csv", row.names = FALSE)
write.csv(edges, file = "edges.csv", row.names = FALSE)
write.csv(all_yanks, file = "yankees.csv", row.names = FALSE)
