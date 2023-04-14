// Collision (en ordonnée) des rectangles
const rectangles_collisions = [100, 210, 323, 435, 545]

for(const rectangle of rectangles_collisions){
  console.log(`Rectangle n°${rectangles_collisions.indexOf(rectangle)+1} => x: 140, y:${rectangles_collisions[rectangles_collisions.indexOf(rectangle)]}, width: 940, height: 90`);
}

console.log("--------------------------------\n\n\nTu devras écrire ")
for(const rectangle of rectangles_collisions){
  console.log(`Rectangle n°${rectangles_collisions.indexOf(rectangle)+1} => pygame(140, ${rectangles_collisions[rectangles_collisions.indexOf(rectangle)]}, 940, 90)`);
}
