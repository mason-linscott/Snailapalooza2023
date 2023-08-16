install.packages(c("ape", "bayou", "phytools", "geiger", "BAMMtools", 
                   "dplyr", "PCMBase", "castor"))

require(ape)

require(bayou)
require(phytools)
require(geiger)
require(BAMMtools)
require(dplyr)
require(PCMBase)
require(castor)

drop.random.extant <- function(phy, m, tol = 1e-8)
{
  n <- Ntip(phy)
  x<-get_all_distances_to_root(phy)[1:n]
  drop.tip(phy, phy$tip.label[sample(which(near(x,max(x))=="TRUE"),m)[1:m]])
}

drop.random.fossil <- function(phy, m, tol = 1e-8)
{
  n <- Ntip(phy)
  x<-get_all_distances_to_root(phy)[1:n]
  drop.tip(phy, phy$tip.label[sample(which(x < max(x) - tol),m)[1:m]])
}

sim.Tree<-function(n_extant,tree_size,max_time,n_tree)
{
  tree_list<-list() #store trees in list
  n_fossil=tree_size-n_extant
  b_modify<-0.1*(n_extant/tree_size)
  p_birth=0.2+b_modify
  p_death=0.2
  
  for(g in 1:n_tree) {
    
    if (n_extant>1) 
    {
      pre_tree<-rphylo(n=n_extant,birth=p_birth,death=p_death,fossils = TRUE) #simulate a tree with fossils
      while(Ntip(pre_tree)<tree_size) #make sure simtree is big enough
      {
        pre_tree<-rphylo(n=n_extant,birth=p_birth,death=p_death,fossils = TRUE)
      }
      tree<-drop.random.fossil(pre_tree,(Ntip(pre_tree)-(tree_size)))
    }
    if (n_extant==tree_size) #drop fossils if simulating ultrametric trees
    { 
      tree<-drop.random.fossil(pre_tree,(Ntip(pre_tree)-(tree_size)))
    }
    
    
    if (n_extant==0) #drop extant tips if simulating only fossils
    {
      n_extant=50
      pre_tree<-try(rphylo(n=n_extant,birth=p_birth,death=p_death,fossils = TRUE),silent=TRUE)
      while((Ntip(pre_tree)-n_extant)<tree_size) #make sure simtree is big enough
      {
        pre_tree<-try(rphylo(n=n_extant,birth=p_birth,death=p_death,fossils = TRUE),silent=TRUE)
      }
      near_tree<-drop.random.extant(pre_tree,n_extant)
      tree<-drop.random.fossil(near_tree, (Ntip(near_tree)-tree_size))
      
    }
    tree$edge.length<-tree$edge.length/max(nodeHeights(tree)[,2])*max_time #scale to time
    
    tree_list[[g]]<-tree
    
  }
  if (length(tree_list)==1) 
  {
    tree<-tree_list[[1]]
    return(tree)
  } 
  else{
    return(tree_list)
  }
}

# Make random tree
#myTree <- ape::rtree(64)

myTree <- sim.Tree(32, 32, 25, 1)

plot(myTree)

# Generate data 
col1 <- as.data.frame(ape::rTraitCont(myTree, sigma = 0.001, root.value=0.99)) 
col2 <- as.data.frame(ape::rTraitCont(myTree, sigma = 0.02, root.value=0.3)) 
col3 <- as.data.frame(ape::rTraitCont(myTree, sigma = 0.4, root.value=12)) 

# Bind data frames
myData <- cbind(col1, col2, col3)

# Change the names
names(myData)[1:3] <- c("coil_fatness", "face_height", "degree_of_coiling")

# Save 
write.csv(myData, file = "treedata.csv")
write.tree(myTree,"snailapalooza.tre")
