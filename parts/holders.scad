sl = 38.5; // servo length
sw = 19; // servo width
sh = 28; // servo height
ss = 8; // servo slot width

bl = 90; // Business card length 
bw = 50; // Business card width 
bh = 10; // Business card height
bs = 18; // Business card slot size

t = 0.4; // tolerance

a = 0.8; // base height
b = 10; // Brim around holders
c = 4; // hole size
d = 4; // Wall thickness
w = 2; // Card holder wall thickness

$fs=0.02;

servo_holder();
translate([0,sw+2*b+2*d+20,0]) card_holder();


module servo_holder () {
    difference() {
        cube ([sl+2*b+2*d+2*t,sw+2*b+2*d+2*t,a]);
translate([0,b+sw/2+d+t,0]) hull() {
        cylinder (a, r=c/2);
        translate([b+d,0,0]) cylinder (a, r=c/2);
}
hull() {
        translate([sl+3*b/2+2*d+2*t,b/2,0]) cylinder (a, r=c/2);
        translate([sl+3*b/2+2*d+2*t,sw+3*b/2+d*2+t*2,0]) cylinder (a, r=c/2);
}
}
    translate([b,b,a]) difference() {
        // Main block
        cube([sl+2*t+2*d,sw+2*t+2*d,sh]);
        //servo
        translate([d,d,0]) cube([sl+2*t,sw+2*t,sh]);
        // servo wire slot
        translate([0,d+sw/2-ss/2,0]) cube([d,ss+2*t,sh]);
    }
}


module card_holder () {
    difference() {
        cube ([bl+2*w+2*t,bw+2*w+2*t,a]);
        translate([0,bw/2+w+t,0]) hull() {
            cylinder (a, r=bs/2);
            translate([w,0,0]) cylinder (a, r=bs/2);
        }
    }
    translate([0,0,a]) difference() {
        // Main block
        cube([bl+2*t+2*w,bw+2*w+2*t,bh]);
        //hole
        translate([w,w,0]) cube([bl+2*t,bw+2*t,bh]);
        // slot
        translate([0,w+bw/2-bs/2,0]) cube([w,bs+2*t,bh]);
    }
}
