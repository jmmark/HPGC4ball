library(tidyr)
roster <- read.csv("../currentRoster.csv")

teamNo <- c(1:20, 1:20)
teamNo <- teamNo[order(teamNo)]
teamNo

roster <- roster[order(roster$Team),]
roster$teamNo <- teamNo
print(roster)

set.seed(2016)
pools <- rep(c("A","B","C","D","E"),4)
pools <- sample(pools,length(pools))
print(pools)

idx <- 1:20
pooler <- data.frame(idx, pools)
print(pooler)

roster <- merge(roster, pooler, by.x="teamNo", by.y="idx")
roster$Name <- paste(roster$First.Name, roster$Last.Name)
write.csv(roster, "../rosterPools.csv",row.names = FALSE)

ppos <- rep(c("Player 1","Player 2"),20)
roster$ppos <- ppos
allPool <- roster[,c("teamNo","Name","pools","ppos")]

allPool <- spread(allPool, ppos, Name)
names(allPool) <- c("Team Number", "Pool", "Player 1", "Player 2")
allPool$Wins <- numeric(20)
allPool$Losses <- numeric(20)
allPool$Ties <- numeric(20)
allPool$Points <- numeric(20)
allPool$'Holes Won' <- numeric(20)

write.csv(allPool,"poolPlay.csv",row.names=FALSE)
