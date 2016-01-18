function out = slash2backslash( in )
out = in;
idx = findstr(out,'/');
out(idx) = '\';
