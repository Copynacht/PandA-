//copyright (c) 2020 Copynight  all rights reserved.

#include<Windows.h>
#include <commctrl.h>
#include<time.h>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>
#include "menu.h"
#define ID_MYTIMER 400
#define Year 2020
#define Month 5
#define Day 19
#define MM_UPDATE 1002
#define MM_HELP 1003
#define ID_MYTRAY 300
#define MYTRAY_MESSAGE (WM_APP +1)
std::string szTasks[200];
int tasks = 0;
typedef void(*DIALOG)(HINSTANCE, HWND, int, int, int, int, int);
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
ATOM WindowClass(HINSTANCE);
BOOL MakeWindow(HINSTANCE, int);
BOOL CALLBACK DllProc(HWND, UINT, WPARAM, LPARAM);
HMENU hMenu;
TCHAR ClassName[] = TEXT("top");
HWND hWndM, button;
HINSTANCE hInstance;
HWND hList;
bool Cmd = 0;
NOTIFYICONDATA ni;
HMENU menu, submenu;
POINT pt;

int WINAPI WinMain(HINSTANCE hInst, HINSTANCE hPrevInst, LPSTR  CmdLine, int CmdShow) {
	MSG msg;
	hInstance = hInst;
	std::ifstream ifs("ApplicationData/data/task.txt");
	if (!ifs)MessageBox(NULL, TEXT("Cant open file."), TEXT("Error"), MB_OK);
	while (ifs && std::getline(ifs, szTasks[tasks])) {
		tasks++;
	}
	if (!WindowClass(hInst))return 0;
	if (!MakeWindow(hInst, CmdShow))return 0;
	while (1) {
		switch (GetMessage(&msg, NULL, 0, 0)) {
		case 0:
			return (int)msg.wParam;
			break;
		case -1:
			return -1;
			break;
		default:
			TranslateMessage(&msg);
			DispatchMessage(&msg);
			break;
		}
	}return 0;
}
ATOM WindowClass(HINSTANCE hInst) {
	WNDCLASSEX wc;
	wc.cbSize = sizeof(WNDCLASSEX);
	wc.style = CS_HREDRAW | CS_VREDRAW;
	wc.lpfnWndProc = WndProc;
	wc.cbWndExtra = 0;
	wc.cbClsExtra = 0;
	wc.hInstance = hInst;
	wc.hIcon = (HICON)LoadImage(hInst, TEXT("MYICON"), IMAGE_ICON, 0, 0, 0);
	wc.hCursor = (HCURSOR)LoadImage(hInst, MAKEINTRESOURCE(IDC_ARROW), IMAGE_CURSOR, NULL, NULL, LR_DEFAULTSIZE);
	wc.hbrBackground = (HBRUSH)CreateSolidBrush(RGB(255, 255, 255));
	wc.lpszMenuName = TEXT("MYMENU");
	wc.lpszClassName = ClassName;
	wc.hIconSm = (HICON)LoadImage(hInst, MAKEINTRESOURCE(IDI_APPLICATION), IMAGE_ICON, NULL, NULL, LR_DEFAULTSIZE);

	return (RegisterClassEx(&wc));
}

BOOL MakeWindow(HINSTANCE hInst, int CmdShow)
{
	hWndM = CreateWindow(ClassName, TEXT("PandA課題一覧"), WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX, CW_USEDEFAULT, CW_USEDEFAULT, 715, 300, NULL, NULL, hInst, NULL);
	button = CreateWindow(TEXT("button"), TEXT("更新"), WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON, 280, 220, 100, 40, hWndM, (HMENU)(MM_UPDATE), hInst, NULL);

	if (!hWndM)return FALSE;
	ShowWindow(hWndM, CmdShow);
	UpdateWindow(hWndM);
	return TRUE;
}
LRESULT CALLBACK WndProc(HWND hWnd, UINT msg, WPARAM wp, LPARAM lp)
{
	STARTUPINFO si = { sizeof(STARTUPINFO) };
	PROCESS_INFORMATION pi = {};
	switch (msg) {
	case WM_CLOSE:
		ShowWindow(hWnd, SW_HIDE);
		Cmd = 1;
		break;
	case MYTRAY_MESSAGE:
		switch (lp) {
		case WM_RBUTTONDOWN:
			menu = LoadMenu(hInstance, TEXT("SUBMENU"));
			if (Cmd == 0)EnableMenuItem(menu, IDM_START, MF_BYCOMMAND | MF_GRAYED);
			submenu = GetSubMenu(menu, 0);
			GetCursorPos(&pt);
			SetForegroundWindow(hWnd);
			TrackPopupMenu(submenu, TPM_BOTTOMALIGN, pt.x, pt.y, 0, hWnd, NULL);
			DestroyMenu(submenu);
			break;
		default:
			return (DefWindowProc(hWnd, msg, wp, lp));
		}
		break;
	case WM_COMMAND:
		switch (LOWORD(wp)) {
		case IDM_START:
			ShowWindow(hWnd, SW_SHOW);
			Cmd = 0;
			break;

		case IDM_HELP:
			DialogBox(hInstance, TEXT("MYDLG"), hWnd, (DLGPROC)DllProc);
			break;
		case IDM_FINISH:
			PostQuitMessage(0);
			break;
		case MM_UPDATE:
			CreateProcess(
				TEXT("ApplicationData/operator.exe"),
				0,
				NULL,
				NULL, FALSE,
				0, NULL,
				TEXT("ApplicationData"),
				&si,
				&pi
				);
			DWORD dwResult = ::WaitForSingleObject(
				pi.hProcess
				,INFINITE
			);
			HWND pyWnd = FindWindow(NULL, TEXT("ApplicationData/operator.exe"));
		    PostMessage(pyWnd, WM_CLOSE, 0, 0);
			::CloseHandle(pi.hProcess);
			::CloseHandle(pi.hThread);

			tasks = 0;
			std::ifstream ifs("ApplicationData/data/task.txt");
			if (!ifs)MessageBox(NULL, TEXT("Cant open file."), TEXT("Error"), MB_OK);
			while (ifs && std::getline(ifs, szTasks[tasks])) {
				tasks++;
			}
			DestroyWindow(hList);
			hList = CreateWindow(TEXT("LISTBOX"), NULL, WS_CHILD | WS_VISIBLE | LBS_STANDARD, 0, 0, 700, 230, hWnd, (HMENU)500, hInstance, NULL);
			for (int x = 0; x < tasks; x++)
				SendMessage(hList, LB_ADDSTRING, 0, (WPARAM)shift_jis_to_utf_16(szTasks[x]).c_str());
			break;
		}
		break;
	case WM_CREATE:
		SetWindowPos(hWnd, HWND_NOTOPMOST, 0, 0, 0, 0, (SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW));
		memset(&ni, 0, sizeof(NOTIFYICONDATA));
		ni.cbSize = sizeof(NOTIFYICONDATA);
		ni.hWnd = hWnd;
		ni.uID = ID_MYTRAY;
		ni.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP;
		ni.hIcon = (HICON)LoadImage(hInstance, TEXT("MYICON"), IMAGE_ICON, 0, 0, 0);
		ni.uCallbackMessage = MYTRAY_MESSAGE;
		Shell_NotifyIcon(NIM_ADD, &ni);
		hList = CreateWindow(TEXT("LISTBOX"), NULL, WS_CHILD | WS_VISIBLE | LBS_STANDARD, 0, 0, 700, 230, hWnd, (HMENU)500, hInstance, NULL);
		for (int x = 0; x < tasks; x++)
			SendMessage(hList, LB_ADDSTRING, 0, (WPARAM)shift_jis_to_utf_16(szTasks[x]).c_str());
		break;
	default:
		return (DefWindowProc(hWnd, msg, wp, lp));
		break;
	}return 0;
}
}