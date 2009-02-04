#include <GL/gl.h>

struct Numeric_Edge
{
	int a,b;
	int len;
	Numeric_Edge(int x, int y,int num)
	{
		if(((x-y+num)%num)<((y-x+num)%num))
		{
			a=y;
			b=x;
			len=((x-y+num)%num);
		}
		else
		{
			a=x;
			b=y;
			len=((y-x+num)%num);
		}
	}
	bool operator<(const Numeric_Edge& e) const
	{
		return len<e.len;
	}
};

class Vector2
{
public:
	int x,y;
	int index;
	int chain;
	Vector2(int a, int b, int i):x(a),y(b),index(i){}
	Vector2(int a, int b):x(a),y(b),index(-1){}
	bool operator==(const Vector2& v){return v.x==x && v.y==y;}
	bool operator==(int i){return index==i;}
	bool operator<(const Vector2& v) const {return (y==v.y)?(x < v.x):(y < v.y);}
	const Vector2 operator-(const Vector2& v)const { return Vector2(x-v.x,y-v.y);}
	const Vector2 operator+(const Vector2& v)const { return Vector2(x+v.x,y+v.y);}
	const Vector2 operator*(int p)const { return Vector2(x*p,y*p);}
	Vector2& operator/=(int v) { x/=v; y/=v; return *this;}

};

class Triangle
{
public:
	Vector2 v1,v2,v3;
	Triangle(Vector2 a,Vector2 b, Vector2 c):v1(a),v2(b),v3(c){}
};

class Edge
{
	friend class Shape;
private:
	int x1,x2;
	int y1,y2;
public:
	int index;
	Edge(const Vector2& a,const Vector2& b, int i):index(i)
	{
		y1=a.y;
		y2=b.y;
		x1=a.x;
		x2=b.x;
	}
	bool yIntersect(int y,int32_t& d)
	{
		int u1,u2;
		u1=min(y1,y2);
		u2=max(y1,y2);
		if((y>=u1) && (y<u2))
		{
			float m=(x2-x1);
			m/=(y2-y1);
			d=m*(y-y1);
			d+=x1;
			return true;
		}
		else
			return false;
	}
	bool xIntersect(int x,int32_t& d)
	{
		int u1,u2;
		u1=min(x1,x2);
		u2=max(x1,x2);
		if((x>=u1) && (x<=u2))
		{
			if(x2==x1)
			{
				d=y1;
			}
			else
			{
				float m=(y2-y1);
				m/=(x2-x1);
				d=m*(x-x1);
				d+=y1;
			}
			return true;
		}
		else
			return false;
	}
	bool operator==(int a)
	{
		return index==a;
	}

};

class Graphic
{
public:
	bool filled0;
	bool filled1;
	bool stroked;
	RGBA color0;
	RGBA color1;
	RGBA stroke_color;
};

class Shape
{
public:
	std::vector<Triangle> interior;
	std::vector<Vector2> outline;
	Graphic graphic;
	bool closed;

	//DEBUG
	std::vector<Edge> edges;
	void Render() const;
};
