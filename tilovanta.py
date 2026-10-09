#!/usr/bin/env python3
"""Tilovanta: turn-based tile path with gaps and jump hazards."""
import argparse,curses,random,collections
from terminal_ui import setup,text,title
class Game:
    size=10
    def __init__(self,seed=None):
        self.rng=random.Random(seed);self.pos=(0,9);self.finish=(9,0);self.moves=0;self.dead=False;self.won=False;self.board={}
        # Guaranteed reachable stair path, all other tiles are randomized.
        self.path={(0,9)};x,y=0,9
        while x<9 or y>0:
            if x<9 and (y==0 or self.rng.randrange(2)):x+=1
            else:y-=1
            self.path.add((x,y))
        for y in range(10):
            for x in range(10):self.board[x,y]='.' if (x,y) in self.path else self.rng.choices(['.',' ','!'],[5,3,2])[0]
    def move(self,dx,dy,jump=False):
        if self.dead or self.won:return False
        if (dx,dy) not in ((1,0),(-1,0),(0,1),(0,-1)):raise ValueError('One cardinal direction required.')
        d=2 if jump else 1;x=self.pos[0]+dx*d;y=self.pos[1]+dy*d
        if not (0<=x<10 and 0<=y<10):return False
        self.pos=(x,y);self.moves+=1;self.dead=self.board[self.pos] in (' ','!');self.won=self.pos==self.finish and not self.dead;return True
    def reachable(self):
        queue=collections.deque([(0,9)]);seen={(0,9)}
        while queue:
            p=queue.popleft()
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                q=p[0]+dx,p[1]+dy
                if q not in seen and self.board.get(q)=='.':seen.add(q);queue.append(q)
        return self.finish in seen

def run(stdscr,seed):
    setup(stdscr);g=Game(seed);jump=False;message='Find the safe path to X. Gaps are blank; ! is a hazard.'
    while True:
        title(stdscr,'Tilovanta',f'Moves {g.moves} | '+('Won! R restarts.' if g.won else 'Fell. R restarts.' if g.dead else 'JUMP2 armed' if jump else 'STEP1'), 'Arrows/WASD | J arm jump | R new board | Q quit')
        h,w=stdscr.getmaxyx()
        if h<18 or w<58:text(stdscr,4,2,'Resize to 58x18. Board retained.',3)
        else:
            cw=max(4,(w-4)//10);rh=max(1,(h-8)//10);left=(w-cw*10)//2
            for y in range(10):
                for x in range(10):
                    p=x,y;v='@' if p==g.pos else 'X' if p==g.finish else g.board[p]
                    for dy in range(rh):text(stdscr,4+y*rh+dy,left+x*cw,'['+(' '*max(1,cw-3))+']',4 if v=='X' else 3 if v=='!' else 2)
                    text(stdscr,4+y*rh+rh//2,left+x*cw+cw//2,v,4 if v=='X' else 3 if v=='!' else 1 if v=='@' else 2,v in ('@','X'))
            text(stdscr,h-3,2,message)
        stdscr.refresh();k=stdscr.getch()
        if k==ord('q'):return
        if k==ord('r'):g=Game(seed);jump=False
        elif k==ord('j') and not g.dead and not g.won:jump=not jump
        elif h>=18 and w>=58:
            d={curses.KEY_UP:(0,-1),ord('w'):(0,-1),curses.KEY_DOWN:(0,1),ord('s'):(0,1),curses.KEY_LEFT:(-1,0),ord('a'):(-1,0),curses.KEY_RIGHT:(1,0),ord('d'):(1,0)}.get(k)
            if d:g.move(*d,jump=jump);jump=False

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--seed',type=int);p.add_argument('--demo',action='store_true');a=p.parse_args()
    if a.demo:
        g=Game(a.seed);print('TILOVANTA\n'+ '\n'.join(''.join('@' if (x,y)==g.pos else 'X' if (x,y)==g.finish else g.board[x,y] for x in range(10)) for y in range(10)));return
    try:curses.wrapper(run,a.seed)
    except curses.error:print('Needs an interactive curses terminal (58x18 minimum).');return 2
    except KeyboardInterrupt:pass
if __name__=='__main__':raise SystemExit(main())
