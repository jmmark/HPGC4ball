library(tidyr)
roster <- read.csv("../currentRoster.csv")

teams_involved <- 20

teamNo <- c(1:teams_involved, 1:teams_involved)
teamNo <- teamNo[order(teamNo)]
teamNo

roster <- roster[order(roster$team_id),]
roster$teamNo <- teamNo
print(roster)

set.seed(2018)
pools <- rep(c("A","B","C","D","E"),4)
pools <- sample(pools,length(pools))
print(pools)

idx <- 1:teams_involved
pooler <- data.frame(idx, pools)
print(pooler)

roster <- merge(roster, pooler, by.x="teamNo", by.y="idx")
roster$Name <- paste(roster$first_name, roster$last_name)
write.csv(roster, "../rosterPools.csv",row.names = FALSE)

ppos <- rep(c("Player 1","Player 2"),teams_involved)
roster$ppos <- ppos
allPool <- roster[,c("teamNo","Name","pools","ppos")]

allPool <- spread(allPool, ppos, Name)
names(allPool) <- c("Team Number", "Pool", "Player 1", "Player 2")
allPool$Wins <- numeric(teams_involved)
allPool$Losses <- numeric(teams_involved)
allPool$Ties <- numeric(teams_involved)
allPool$Points <- numeric(teams_involved)
allPool$'Holes Won' <- numeric(teams_involved)

write.csv(allPool,"poolPlay.csv",row.names=FALSE)
