imgdir="/Users/thomaslinscott/Downloads/cutimages"
pdf(width=10,height=10)
ggtree(snailtree,layout = "circular")  +
     geom_tiplab(aes(image=paste0(imgdir, '/', label, '.png')), geom="image",offset=2,angle=90)
dev.off()