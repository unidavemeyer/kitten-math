# kitten-math
Education/game to rescue kittens by solving math problems. Initial ideas:

 * kitten in a cage; as timer expires, locks appear; as problems solve, locks disappear
 * timer counts down from 10 (or whatever) seconds; once problem is answered, remaining seconds worth of kittens escape

Next steps:

 * Set up so that we take arguments for who is playing (easier than a UI for that for now)
 * Figure out how to not let stop/play nerf the overall experience
 * Make sure to also log problems that weren't successfully answered at all (we miss those right now, but those are critical to track)

Future looking but not to implement right now:

 * Would be fun to look into 500/1000 rescue goals, maybe
 * Would be super valuable to weight trickier problems to have higher likelihood
 * Would be fun to add an actual little graphic of some kind showing kittens disappearing or something
