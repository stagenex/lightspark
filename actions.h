#include "tags.h"
#include "frame.h"
#include <vector>

class ActionTag
{
public:
	virtual void Execute()=0;
	virtual void print()=0;
};

class DoActionTag: public DisplayListTag
{
private:
	std::vector<ActionTag*> actions;
public:
	DoActionTag(RECORDHEADER h, std::istream& in);
	void Render( );
	UI16 getDepth();
	void printInfo();
};

class ACTIONRECORDHEADER
{
public:
	UI8 ActionCode;
	UI16 Length;
	ACTIONRECORDHEADER(std::istream& in);
	ActionTag* createTag(std::istream& in);
};

class ActionStop:public ActionTag
{
public:
	void Execute();
	void print(){ std::cout  << "ActionStop" << std::endl;}
};

class ActionJump:public ActionTag
{
private:
	SI16 BranchOffset;
public:
	ActionJump(std::istream& in);
	void Execute();
	void print(){ std::cout  << "ActionJump" << std::endl;}
};

class ActionIf:public ActionTag
{
private:
	SI16 Offset;
public:
	ActionIf(std::istream& in);
	void Execute();
	void print(){ std::cout  << "ActionIf" << std::endl;}
};

class ActionGotoFrame:public ActionTag
{
private:
	UI16 Frame;
public:
	ActionGotoFrame(std::istream& in);
	void Execute();
	void print(){ std::cout  << "ActionGotoFrame" << std::endl;}
};

class ActionGetURL:public ActionTag
{
private:
	STRING UrlString;
	STRING TargetString;
public:
	ActionGetURL(std::istream& in);
	void Execute();
	void print(){ std::cout  << "ActionGetURL" << std::endl;}
};

class ActionConstantPool : public ActionTag
{
private:
	UI16 Count;
	std::vector<STRING> ConstantPool;
public:
	ActionConstantPool(std::istream& in);
	void Execute();
	void print(){ std::cout  << "ActionConstantPool" << std::endl;}
};

class ActionStringAdd: public ActionTag
{
public:
	void Execute();
	void print(){ std::cout  << "ActionStringAdd" << std::endl;}
};

class ActionStringExtract: public ActionTag
{
public:
	void Execute();
	void print(){ std::cout  << "ActionStringExtract" << std::endl;}
};

class ActionNot: public ActionTag
{
public:
	void Execute();
	void print(){ std::cout  << "ActionNot" << std::endl;}
};

class ActionStringEquals: public ActionTag
{
public:
	void Execute();
	void print(){ std::cout  << "ActionStringEquals" << std::endl;}
};

class ActionSetVariable: public ActionTag
{
public:
	void Execute();
	void print(){ std::cout  << "ActionSetVariable" << std::endl;}
};

class ActionGetVariable: public ActionTag
{
public:
	void Execute();
	void print(){ std::cout  << "ActionGetVariable" << std::endl;}
};

class ActionToggleQuality: public ActionTag
{
public:
	void Execute();
};

class ActionPush : public ActionTag
{
private:
	UI8 Type;
	STRING String;
	//FLOAT Float;
	UI8 RegisterNumber;
	UI8 Boolean;
	//DOUBLE Double;
	UI32 Integer;
	UI8 Constant8;
	UI16 Constant16;
public:
	ActionPush(std::istream& in,ACTIONRECORDHEADER* h);
	void Execute();
	void print(){ std::cout  << "ActionPush" << std::endl;}
};

class BUTTONCONDACTION
{
public:
	UI16 CondActionSize;
	UB CondIdleToOverDown;
	UB CondOutDownToIdle;
	UB CondOutDownToOverDown;
	UB CondOverDownToOutDown;
	UB CondOverDownToOverUp;
	UB CondOverUpToOverDown;
	UB CondOverUpToIdle;
	UB CondIdleToOverUp;
	UB CondKeyPress;
	UB CondOverDownToIdle;
	std::vector<ActionTag*> Actions;
	
	bool isLast()
	{
		return !CondActionSize;
	}
};

std::istream& operator>>(std::istream& stream, BUTTONCONDACTION& v);